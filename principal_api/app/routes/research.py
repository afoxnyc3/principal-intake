from fastapi import APIRouter, HTTPException

from app.models.request_models import ResearchRequest
from app.models.response_models import ResearchResponse
from app.services.researcher import research

router = APIRouter()


@router.post("/research-agenda", response_model=ResearchResponse)
def research_agenda(request: ResearchRequest):
    try:
        result = research(request.text)
        return ResearchResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM service error: {e}")
