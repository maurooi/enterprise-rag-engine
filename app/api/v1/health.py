from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import APIRouter, Depends, Response, status

from app.api.v1.schemas import HealthResponse
from app.core.config import Settings, get_settings
from app.db.session import get_db_session

router = APIRouter(prefix="/api/v1", tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health(
    response: Response,
    settings: Annotated[Settings, Depends(get_settings)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> HealthResponse:
    try:
        await session.execute(
            text("SELECT 1")
        )
        health_status = "ok"
        database = "ready"
        
    except Exception:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        health_status = "degraded"
        database = "disconnected"

    return HealthResponse(
            app_name=settings.app_name,
            environment=settings.app_env,
            version=settings.app_version,
            status=health_status,
            database=database,
        )
