from pydantic import BaseModel


class HealthResponse(BaseModel):
    app_name: str
    environment: str
    version: str
    status: str
