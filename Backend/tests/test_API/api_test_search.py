from fastapi.testclient import TestClient

from app.__main__ import app

client = TestClient(app)


def get_search_by_name(name: str, headers: dict):
    return client.get(f"/search/?name={name}", headers=headers)
