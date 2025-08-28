from fastapi import FastAPI
from datetime import datetime
from common.schemas import PredictionRequest, OutputEnvelope, MainResponse, MainContent, Prediction, PerformanceMetrics, SystemMetadata
import time, random

app = FastAPI(title="Prediction Service", version="0.1.0")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "prediction"}

@app.post("/predict", response_model=OutputEnvelope)
async def predict(req: PredictionRequest):
    t0 = time.perf_counter()
    prob = round(random.uniform(0.4, 0.95), 2)
    band = "A" if prob>0.85 else "B" if prob>0.7 else "C" if prob>0.55 else "D"
    pred = [Prediction(subject=req.context.get("subject", "math"), horizon_days=30, prob_pass=prob, band=band)]

    content = MainContent(mastery_vector=[], gaps=[], curriculum_plan=None, predictions=pred)
    perf = PerformanceMetrics(latency_ms=int((time.perf_counter()-t0)*1000), processing_ms=int((time.perf_counter()-t0)*1000), cost_units=0.005)
    sys = SystemMetadata(model_info="pred-baseline", strategy_info="logit-mock", timestamp=datetime.utcnow())

    return OutputEnvelope(
        primary_id=req.student_profile.get("id", "opaque"),
        main_response=MainResponse(content=content, uncertainty_factors=["data_missing"]),
        supporting_data=[],
        performance_metrics=perf,
        system_metadata=sys,
    )
