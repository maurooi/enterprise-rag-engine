from collections.abc import AsyncIterator
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.db.session import get_db_session
from app.main import app

client = TestClient(app)


async def override_db_down() -> AsyncIterator[AsyncMock]:
    mock_session = AsyncMock()
    mock_session.execute.side_effect = ConnectionError("DB unreachable")
    yield mock_session


async def override_db_up() -> AsyncIterator[AsyncMock]:
    mock_session = AsyncMock()
    yield mock_session


def test_health_db_up() -> None:
    app.dependency_overrides[get_db_session] = override_db_up
    try:
        response = client.get("/api/v1/health")
        settings = get_settings()

        assert response.status_code == 200
        data = response.json()
        assert data["app_name"] == settings.app_name
        assert data["environment"] == settings.app_env
        assert data["version"] == settings.app_version
        assert data["app_status"] == "ok"
        assert data["database_status"] == "ready"
    finally:
        app.dependency_overrides.clear()


def test_health_db_down() -> None:
    app.dependency_overrides[get_db_session] = override_db_down
    try:
        response = client.get("/api/v1/health")
        settings = get_settings()

        assert response.status_code == 503
        data = response.json()
        assert data["app_name"] == settings.app_name
        assert data["environment"] == settings.app_env
        assert data["version"] == settings.app_version
        assert data["app_status"] == "degraded"
        assert data["database_status"] == "disconnected"
    finally:
        app.dependency_overrides.clear()
