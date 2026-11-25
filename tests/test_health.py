from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/v1/health")
    settings = get_settings()

    assert response.status_code == 200
    data = response.json()
    assert data["app_name"] == settings.app_name
    assert data["environment"] == settings.app_env
    assert data["version"] == settings.app_version
    assert data["status"] == "ok"
