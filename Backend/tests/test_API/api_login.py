from fastapi.testclient import TestClient
from src.main import app as app

client = TestClient(app)


def post_login(user_name: str, password: str):
    data = {"username": user_name, "password": password}
    response = client.post(f"/login", data=data)
    return response
