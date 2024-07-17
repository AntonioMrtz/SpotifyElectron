from fastapi.testclient import TestClient
from httpx import Response

from app.__main__ import app

client = TestClient(app)


def get_search_by_name(name: str, headers: dict[str, str]) -> Response:
    return client.get(f"/search/?name={name}", headers=headers)
