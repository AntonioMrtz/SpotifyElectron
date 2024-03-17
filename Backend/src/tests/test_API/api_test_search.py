from main import app as app
from fastapi.testclient import TestClient

client = TestClient(app)


def get_search_by_name(name: str, headers: dict):

    response = client.get(f"/search/?nombre={name}", headers=headers)
    return response
