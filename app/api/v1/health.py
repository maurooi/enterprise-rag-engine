from typing import Annotated
import logging

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas import HealthResponse
from app.core.config import Settings, get_settings
from app.db.session import get_db_session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health(
    response: Response,
    settings: Annotated[Settings, Depends(get_settings)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> HealthResponse:
    try:
        await session.execute(text("SELECT 1"))
        app_status = "ok"
        database_status = "ready"

    except Exception:
        logger.warning("Database healthcheck failed", exc_info=True)
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        app_status = "degraded"
        database_status = "disconnected"

    return HealthResponse(
        app_name=settings.app_name,
        environment=settings.app_env,
        version=settings.app_version,
        app_status=app_status,
        database_status=database_status,
    )
