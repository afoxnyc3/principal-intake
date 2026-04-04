from fastapi import APIRouter, HTTPException

from app.models.request_models import SummarizeRequest
from app.models.response_models import SummarizeResponse
from app.services.summarizer import summarize

router = APIRouter()


@router.post("/summarize", response_model=SummarizeResponse)
def summarize_idea(request: SummarizeRequest):
    try:
        summary = summarize(
            text=request.text,
            max_length=request.max_length,
            context=request.context.value,
        )
        return SummarizeResponse(summary=summary)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM service error: {e}")
