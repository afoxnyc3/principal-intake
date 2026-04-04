from fastapi import APIRouter, HTTPException

from app.models.request_models import ClassifyRequest
from app.models.response_models import ClassifyResponse
from app.services.classifier import classify

router = APIRouter()


@router.post("/classify-idea", response_model=ClassifyResponse)
def classify_idea(request: ClassifyRequest):
    try:
        result = classify(request.text)
        return ClassifyResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM service error: {e}")
