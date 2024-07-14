from fastapi.testclient import TestClient
from httpx import Response

from app.__main__ import app

client = TestClient(app)


def post_login(user_name: str, password: str) -> Response:
    data = {"username": user_name, "password": password}
    return client.post("/login", data=data)
