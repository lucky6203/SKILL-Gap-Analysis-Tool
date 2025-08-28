from fastapi import FastAPI
from datetime import datetime
from common.schemas import CurriculumRequest, OutputEnvelope, MainResponse, MainContent, Activity, Objective, PerformanceMetrics, SystemMetadata
import time

app = FastAPI(title="Curriculum Service", version="0.1.0")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "curriculum"}

@app.post("/plan", response_model=OutputEnvelope)
async def plan(req: CurriculumRequest):
    t0 = time.perf_counter()
    objectives = [
        Objective(id="obj1", skill_id=s.skill_id, target_score=max(0.8, s.score+0.1))
        for s in req.mastery_vector
    ]
    activities = [
        Activity(id=f"act-{i+1}", label="Video lesson", estimated_minutes=20, skill_refs=[o.skill_id])
        for i,o in enumerate(objectives)
    ]
    content = MainContent(
        mastery_vector=req.mastery_vector,
        gaps=[],
        curriculum_plan={
            "objectives": [o.model_dump() for o in objectives],
            "activities": [a.model_dump() for a in activities],
            "rationale": "Prerequisite-aware baseline plan"
        },
        predictions=None
    )
    perf = PerformanceMetrics(latency_ms=int((time.perf_counter()-t0)*1000), processing_ms=int((time.perf_counter()-t0)*1000), cost_units=0.01)
    sys = SystemMetadata(model_info="curriculum-greedy", strategy_info="rule-sequencer", timestamp=datetime.utcnow())
    return OutputEnvelope(
        primary_id="opaque",
        main_response=MainResponse(content=content, uncertainty_factors=[]),
        supporting_data=[],
        performance_metrics=perf,
        system_metadata=sys,
    )
