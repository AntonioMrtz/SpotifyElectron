from fastapi.testclient import TestClient
from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_503_SERVICE_UNAVAILABLE,
)

from app.__main__ import app

client = TestClient(app)


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    """Fixture to set up the test environment for the health check tests."""
    pass


def test_health_chec_success():
    response = client.get("/health/")
    assert response.status_code == HTTP_200_OK
    assert response.text == "OK"


def test_health_check_database_unhealty(mocker):
    """Test health endpoint returns appropriate error when database is unhealthy."""

    async def mock_check_database_health():
        return False

    mocker.patch(
        "app.database.DatabaseConnectionManager.DatabaseConnectionManager.check_database_health",
        side_effect=mock_check_database_health,
    )
    response = client.get("/health/")
    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_health_check_database_ping_exception(mocker):
    """Test health endpoint returns 503 when database raises ping exception."""

    async def mock_health_check_exception():
        from app.database.database_schema import DatabasePingFailedError

        raise DatabasePingFailedError()

    mocker.patch(
        "app.database.DatabaseConnectionManager.DatabaseConnectionManager.check_database_health",
        side_effect=mock_health_check_exception,
    )

    response = client.get("/health/")
    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE


def test_health_check_song_service_exception(mocker):
    """Test health endpoint returns 503 when song service raises health check exception."""

    def mock_song_service_exception():
        from app.spotify_electron.song.base_song_schema import SongServiceHealthCheckError

        raise SongServiceHealthCheckError()

    mocker.patch(
        "app.spotify_electron.song.providers.song_service_provider.SongServiceProvider.check_service_health",
        side_effect=mock_song_service_exception,
    )
    response = client.get("/health/")
    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE


def test_health_check_auth_service_exception(mocker):
    """Test health endpoint returns 503 when auth service raises health check exception."""

    def mock_auth_service_exception():
        from app.auth.auth_schema import AuthServiceHealthCheckError

        raise AuthServiceHealthCheckError()

    mocker.patch(
        "app.auth.auth_schema.AuthConfig.check_auth_health",
        side_effect=mock_auth_service_exception,
    )
    response = client.get("/health/")
    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE


def test_health_check_multiple_services_unhealthy(mocker):
    """Test health endpoint returns 500 when multiple services are unhealthy."""

    async def mock_check_database_health():
        return False

    mocker.patch(
        "app.database.DatabaseConnectionManager.DatabaseConnectionManager.check_database_health",
        side_effect=mock_check_database_health,
    )
    mocker.patch(
        "app.spotify_electron.song.providers.song_service_provider.SongServiceProvider.check_service_health",
        return_value=False,
    )
    response = client.get("/health/")
    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR


def test_health_check_mixed_service_states(mocker):
    """Test health endpoint handles mixed service states correctly."""

    async def mock_check_database_health():
        return True

    mocker.patch(
        "app.database.DatabaseConnectionManager.DatabaseConnectionManager.check_database_health",
        side_effect=mock_check_database_health,
    )
    mocker.patch(
        "app.spotify_electron.song.providers.song_service_provider.SongServiceProvider.check_service_health",
        return_value=False,
    )
    mocker.patch(
        "app.auth.auth_schema.AuthConfig.check_auth_health",
        return_value=True,
    )
    response = client.get("/health/")
    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
