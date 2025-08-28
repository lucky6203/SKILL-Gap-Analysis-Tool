from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx, os, time
from common.schemas import (
    DiagnoseRequest, CurriculumRequest, PredictionRequest, OutputEnvelope,
    PerformanceMetrics, SystemMetadata, MainResponse, MainContent
)
from datetime import datetime

app = FastAPI(title="API Gateway", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DIAG_URL = os.getenv("DIAG_URL", "http://localhost:8001")
CURR_URL = os.getenv("CURR_URL", "http://localhost:8002")
PRED_URL = os.getenv("PRED_URL", "http://localhost:8003")
ING_URL  = os.getenv("ING_URL",  "http://localhost:8004")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "gateway"}

@app.post("/diagnose", response_model=OutputEnvelope)
async def diagnose(req: DiagnoseRequest):
    t0 = time.perf_counter()
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(f"{DIAG_URL}/diagnose", json=req.model_dump())
    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text)
    data = r.json()
    # Gateway enrich metadata
    perf = PerformanceMetrics(latency_ms=int((time.perf_counter()-t0)*1000), processing_ms=data.get("performance_metrics", {}).get("processing_ms", 0), cost_units=0.0)
    return OutputEnvelope(
        primary_id=data.get("primary_id", "opaque"),
        main_response=MainResponse(**data.get("main_response", {})),
        supporting_data=data.get("supporting_data", []),
        performance_metrics=perf,
        system_metadata=SystemMetadata(model_info="gateway:proxy", strategy_info="pass-through", timestamp=datetime.utcnow())
    )

@app.post("/curriculum", response_model=OutputEnvelope)
async def curriculum(req: CurriculumRequest):
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(f"{CURR_URL}/plan", json=req.model_dump())
    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text)
    return r.json()

@app.post("/predict", response_model=OutputEnvelope)
async def predict(req: PredictionRequest):
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(f"{PRED_URL}/predict", json=req.model_dump())
    if r.status_code != 200:
        raise HTTPException(r.status_code, r.text)
    return r.json()
