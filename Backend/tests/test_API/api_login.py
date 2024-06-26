from fastapi.testclient import TestClient

from app.__main__ import app

client = TestClient(app)


def post_login(user_name: str, password: str):
    data = {"username": user_name, "password": password}
    return client.post("/login", data=data)
