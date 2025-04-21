from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

from app.__main__ import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health/")
    assert response.status_code == HTTP_200_OK
    assert response.text == "OK"


def test_health_check_failure(mocker):
    """Test health endpoint returns appropriate error when database is unhealthy."""
    mocker.patch(
        "app.database.DatabaseConnectionManager.DatabaseConnectionManager.check_database_health",
        return_value=False,
    )
    response = client.get("/health/")
    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE
