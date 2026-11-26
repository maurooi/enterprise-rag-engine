from typing import Literal, Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    app_name: str
    environment: Literal["development", "staging", "production"]
    version: str
    status: Literal["ok", "degraded"]
    database: Literal["ready", "disconnected"]
