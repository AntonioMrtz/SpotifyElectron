from fastapi.testclient import TestClient
from pytest import fixture
from src.main import app


@fixture(scope="module")
def trigger_app_start():
    with TestClient(app):
        yield
