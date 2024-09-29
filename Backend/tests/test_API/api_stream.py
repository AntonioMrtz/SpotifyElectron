from fastapi.testclient import TestClient
from httpx import Response

from app.__main__ import app

client = TestClient(app)


def stream_song(name: str, headers: dict[str, str]) -> Response:
    return client.get(f"/stream/{name}", headers=headers)
