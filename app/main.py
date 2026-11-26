from fastapi import FastAPI
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from app.api.v1 import health
from app.core.config import get_settings
from app.db.session import engine

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await engine.dispose()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(health.router)
