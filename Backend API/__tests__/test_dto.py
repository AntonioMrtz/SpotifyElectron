from fastapi.testclient import TestClient
import logging

from main import app as app

client = TestClient(app)


def test_read_main():
    response = client.get("/playlists/")
    assert response.status_code == 200
    print(response.json())

