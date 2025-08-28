from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from datetime import datetime

class SkillScore(BaseModel):
    skill_id: str
    score: float = Field(ge=0.0, le=1.0)

class Gap(BaseModel):
    skill_id: str
    severity: Literal["low", "med", "high"]

class Objective(BaseModel):
    id: str
    skill_id: str
    target_score: float = Field(ge=0.0, le=1.0, default=0.8)

class Activity(BaseModel):
    id: str
    label: str
    estimated_minutes: int = 30
    skill_refs: List[str]

class Prediction(BaseModel):
    subject: str
    horizon_days: int
    prob_pass: float = Field(ge=0.0, le=1.0)
    band: Literal["A", "B", "C", "D"]

class MetadataKV(BaseModel):
    key: str
    value: str

class Location(BaseModel):
    offset: int
    span: int

class SupportingDatum(BaseModel):
    reference: str
    location: Location
    id: str
    excerpt: str
    relevance: float
    quality: float
    method: Literal["heuristic", "ml", "rule"]

class PerformanceMetrics(BaseModel):
    latency_ms: int
    processing_ms: int
    cost_units: float

class SystemMetadata(BaseModel):
    model_info: str
    strategy_info: str
    timestamp: datetime

class MainContent(BaseModel):
    mastery_vector: List[SkillScore]
    gaps: List[Gap]
    curriculum_plan: Optional[dict]
    predictions: Optional[List[Prediction]]

class MainResponse(BaseModel):
    content: MainContent
    metadata: List[MetadataKV] = []
    confidence_score: float = Field(ge=0.0, le=1.0, default=0.7)
    uncertainty_factors: List[str] = []

class OutputEnvelope(BaseModel):
    primary_id: str
    main_response: MainResponse
    supporting_data: List[SupportingDatum] = []
    performance_metrics: PerformanceMetrics
    system_metadata: SystemMetadata

# Request payloads
class DiagnoseRequest(BaseModel):
    student_profile: dict
    context: dict
    responses: List[dict]
    constraints: Optional[dict] = None
    options: Optional[dict] = None

class CurriculumRequest(BaseModel):
    mastery_vector: List[SkillScore]
    constraints: Optional[dict] = None
    options: Optional[dict] = None

class PredictionRequest(BaseModel):
    student_profile: dict
    context: dict
    features: Optional[dict] = None
