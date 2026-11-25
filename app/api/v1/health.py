from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.v1.schemas import HealthResponse
from app.core.config import Settings, get_settings

router = APIRouter(prefix="/api/v1", tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health(settings: Annotated[Settings, Depends(get_settings)]) -> HealthResponse:
    return HealthResponse(
        app_name=settings.app_name,
        environment=settings.app_env,
        version=settings.app_version,
        status="ok",
    )
