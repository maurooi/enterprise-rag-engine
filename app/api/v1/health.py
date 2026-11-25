from fastapi import APIRouter

from app.api.v1.models import HealthResponse
from app.core.config import get_settings

settings = get_settings()

router = APIRouter(prefix="/api/v1", tags=["Health", "v1"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        app_name=settings.app_name, environment=settings.app_env, version=settings.version, status="ok"
    )
