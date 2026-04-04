from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class IdeaTypeEnum(str, Enum):
    client_opportunity = "client_opportunity"
    internal_build = "internal_build"
    research = "research"
    business_development = "business_development"
    process_improvement = "process_improvement"


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime


class SummarizeResponse(BaseModel):
    summary: str


class ClassifyResponse(BaseModel):
    type: IdeaTypeEnum
    confidence: float
    next_step: str


class ResearchResponse(BaseModel):
    questions: list[str]
    rationale: str
