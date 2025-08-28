from fastapi import FastAPI
from datetime import datetime
import time, random
from common.schemas import DiagnoseRequest, OutputEnvelope, MainResponse, MainContent, SkillScore, Gap, PerformanceMetrics, SystemMetadata

app = FastAPI(title="Diagnostics Service", version="0.1.0")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "diagnostics"}

@app.post("/diagnose", response_model=OutputEnvelope)
async def diagnose(req: DiagnoseRequest):
    t0 = time.perf_counter()
    # Mock scoring (replace with real alignment + ML pipeline later)
    skills = ["skill:fractions.add", "skill:algebra.linear", "skill:reading.infer"]
    mv = [SkillScore(skill_id=s, score=round(random.uniform(0.3, 0.95), 2)) for s in skills]
    gaps = [Gap(skill_id=s.skill_id, severity=("low" if s.score>0.75 else "med" if s.score>0.55 else "high")) for s in mv]

    content = MainContent(mastery_vector=mv, gaps=gaps, curriculum_plan=None, predictions=None)

    perf = PerformanceMetrics(
        latency_ms=int((time.perf_counter()-t0)*1000),
        processing_ms=int((time.perf_counter()-t0)*1000),
        cost_units=0.01,
    )
    sys = SystemMetadata(model_info="diag-baseline", strategy_info="heuristic", timestamp=datetime.utcnow())

    return OutputEnvelope(
        primary_id=req.student_profile.get("id", "opaque"),
        main_response=MainResponse(content=content, uncertainty_factors=["cold_start"], confidence_score=0.72),
        supporting_data=[],
        performance_metrics=perf,
        system_metadata=sys,
    )
