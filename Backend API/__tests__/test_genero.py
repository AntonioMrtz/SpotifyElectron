from fastapi.testclient import TestClient
import logging

from main import app as app

client = TestClient(app)


def test_get_generos_correct():
    response = client.get(f"/generos/")
    assert response.status_code == 200
