from fastapi.testclient import TestClient
from pytest import fixture

from app.__main__ import app

client = TestClient(app)


@fixture(scope="module", autouse=True)
def set_up(trigger_app_start):
    pass


def test_health_check():
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.text == "OK"
