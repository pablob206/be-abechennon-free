"""Test setup"""
# Third-Party
import pytest
from fastapi.testclient import TestClient

# App
from main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Test client"""
    return TestClient(app)
