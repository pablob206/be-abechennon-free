"""Test Main routes"""

# Third-Party
from fastapi.testclient import TestClient

# App
from app.config import settings


def test_root(client: TestClient) -> None:
    """Test root"""

    response = client.get(f"{settings.API_V1_STR}/")
    response.raise_for_status()
    data = {
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
    }

    assert response.json() == data
