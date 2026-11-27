from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    app_name: str
    environment: Literal["development", "staging", "production"]
    version: str
    app_status: Literal["ok", "degraded"]
    database_status: Literal["ready", "disconnected"]
