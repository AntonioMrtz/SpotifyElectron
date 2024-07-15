from fastapi.testclient import TestClient
from pytest import fixture
from starlette.status import HTTP_200_OK

from app.__main__ import app

client = TestClient(app)


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


def test_health_check():
    response = client.get("/health/")
    assert response.status_code == HTTP_200_OK
    assert response.text == "OK"
