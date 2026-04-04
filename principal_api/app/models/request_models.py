from enum import Enum

from pydantic import BaseModel


class ContextEnum(str, Enum):
    client_opportunity = "client_opportunity"
    internal_build = "internal_build"
    research = "research"
    business_development = "business_development"
    process_improvement = "process_improvement"
    general = "general"


class SummarizeRequest(BaseModel):
    text: str
    max_length: int = 140
    context: ContextEnum = ContextEnum.general


class ClassifyRequest(BaseModel):
    text: str


class ResearchRequest(BaseModel):
    text: str
