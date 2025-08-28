from fastapi import FastAPI, UploadFile, File, Form
from datetime import datetime
from common.schemas import OutputEnvelope, MainResponse, MainContent, PerformanceMetrics, SystemMetadata
import time

app = FastAPI(title="Ingestion Service", version="0.1.0")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ingestion"}

@app.post("/upload", response_model=OutputEnvelope)
async def upload(dataset: UploadFile = File(...), source: str = Form("manual")):
    t0 = time.perf_counter()
    # NOTE: this is a stub. In production, parse + validate rows, emit to queue.
    content = MainContent(mastery_vector=[], gaps=[], curriculum_plan=None, predictions=None)
    perf = PerformanceMetrics(latency_ms=int((time.perf_counter()-t0)*1000), processing_ms=int((time.perf_counter()-t0)*1000), cost_units=0.02)
    sys = SystemMetadata(model_info="ingest-v0", strategy_info=f"source={source}", timestamp=datetime.utcnow())
    return OutputEnvelope(primary_id="dataset", main_response=MainResponse(content=content), supporting_data=[], performance_metrics=perf, system_metadata=sys)
