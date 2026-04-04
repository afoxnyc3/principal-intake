from datetime import datetime, timezone

from fastapi import APIRouter

from app.models.response_models import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", timestamp=datetime.now(timezone.utc))
