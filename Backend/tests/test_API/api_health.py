from fastapi.testclient import TestClient
from httpx import Response

from app.__main__ import app

client = TestClient(app)


def health_check() -> Response:
    return client.get("/health/")
