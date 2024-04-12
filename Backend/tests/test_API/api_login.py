from app.__main__ import app
from fastapi.testclient import TestClient

client = TestClient(app)


def post_login(user_name: str, password: str):
    data = {"username": user_name, "password": password}
    response = client.post("/login", data=data)
    return response
