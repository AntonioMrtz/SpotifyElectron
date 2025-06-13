from fastapi.testclient import TestClient
from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_503_SERVICE_UNAVAILABLE,
)

from app.__main__ import app
from tests.test_API.api_health import health_check

client = TestClient(app)


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


def test_health_check_success():
    response = health_check()
    assert response.status_code == HTTP_200_OK
    assert response.text == "OK"


def test_health_check_database_ping_exception(mocker):
    """Test health endpoint returns 503 when database raises ping exception."""

    async def mock_health_check_exception():
        from app.database.database_schema import DatabasePingFailedError

        raise DatabasePingFailedError()

    mocker.patch(
        "app.database.DatabaseConnectionManager.DatabaseConnectionManager.check_database_health",
        side_effect=mock_health_check_exception,
    )

    response = health_check()
    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE


def test_health_check_song_service_exception(mocker):
    """Test health endpoint returns 503 when song service raises health check exception."""

    def mock_song_service_exception():
        from app.spotify_electron.song.base_song_schema import SongServiceHealthCheckError

        raise SongServiceHealthCheckError()

    mocker.patch(
        "app.spotify_electron.song.providers.song_service_provider.SongServiceProvider.check_song_service_health",
        side_effect=mock_song_service_exception,
    )
    response = health_check()
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
    response = health_check()
    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE


def test_health_check_multiple_services_unhealthy(mocker):
    """Test health endpoint returns 500 when multiple services are unhealthy."""

    async def mock_health_check_exception():
        from app.database.database_schema import DatabasePingFailedError

        raise DatabasePingFailedError()

    mocker.patch(
        "app.database.DatabaseConnectionManager.DatabaseConnectionManager.check_database_health",
        side_effect=mock_health_check_exception,
    )
    mocker.patch(
        "app.spotify_electron.song.providers.song_service_provider.SongServiceProvider.check_song_service_health",
        return_value=None,
    )
    response = health_check()
    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE


def test_health_check_mixed_service_states(mocker):
    """Test health endpoint handles mixed service states correctly."""

    async def mock_check_database_health():
        return None

    def mock_song_service_exception():
        from app.spotify_electron.song.base_song_schema import SongServiceHealthCheckError

        raise SongServiceHealthCheckError()

    mocker.patch(
        "app.spotify_electron.song.providers.song_service_provider.SongServiceProvider.check_song_service_health",
        side_effect=mock_song_service_exception,
    )

    mocker.patch(
        "app.database.DatabaseConnectionManager.DatabaseConnectionManager.check_database_health",
        side_effect=mock_check_database_health,
    )

    mocker.patch(
        "app.auth.auth_schema.AuthConfig.check_auth_health",
        return_value=None,
    )
    response = health_check()
    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE
