from fastapi.testclient import TestClient
from pytest import fixture
from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

from app.__main__ import app

client = TestClient(app)


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


def mock_check_database_connection():
    return {"status": "healthy", "message": "Mocked database connection is active"}


def mock_check_song_service():
    return {"status": "healthy", "message": "Mocked SongService is properly initialized"}


def mock_check_auth_config():
    return {
        "status": "healthy",
        "message": "Mocked Auth configuration is properly initialized",
    }


def test_health_check_all_healthy(mocker):
    mocker.patch(
        "app.spotify_electron.health.health_controller.check_database_connection",
        return_value=mock_check_database_connection(),
    )
    mocker.patch(
        "app.spotify_electron.health.health_controller.check_song_service",
        return_value=mock_check_song_service(),
    )
    mocker.patch(
        "app.spotify_electron.health.health_controller.check_auth_config",
        return_value=mock_check_auth_config(),
    )

    response = client.get("/health/")
    assert response.status_code == HTTP_200_OK
    response_json = response.json()

    assert response_json["status"] == "healthy"
    assert response_json["details"]["database"]["status"] == "healthy"
    assert response_json["details"]["song_service"]["status"] == "healthy"
    assert response_json["details"]["auth_config"]["status"] == "healthy"


def test_health_check_unhealthy_database(mocker):
    mocker.patch(
        "app.spotify_electron.health.health_controller.check_database_connection",
        return_value={"status": "unhealthy", "message": "Mocked database connection failed"},
    )
    mocker.patch(
        "app.spotify_electron.health.health_controller.check_song_service",
        return_value=mock_check_song_service(),
    )
    mocker.patch(
        "app.spotify_electron.health.health_controller.check_auth_config",
        return_value=mock_check_auth_config(),
    )

    response = client.get("/health/")
    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE
    response_json = response.json()

    assert response_json["status"] == "unhealthy"
    assert response_json["details"]["database"]["status"] == "unhealthy"
    assert (
        response_json["details"]["database"]["message"] == "Mocked database connection failed"
    )
    assert response_json["details"]["song_service"]["status"] == "healthy"
    assert response_json["details"]["auth_config"]["status"] == "healthy"


def test_health_check_unhealthy_song_service(mocker):
    mocker.patch(
        "app.spotify_electron.health.health_controller.check_database_connection",
        return_value=mock_check_database_connection(),
    )
    mocker.patch(
        "app.spotify_electron.health.health_controller.check_song_service",
        return_value={
            "status": "unhealthy",
            "message": "Mocked SongService initialization failed",
        },
    )
    mocker.patch(
        "app.spotify_electron.health.health_controller.check_auth_config",
        return_value=mock_check_auth_config(),
    )

    response = client.get("/health/")
    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE
    response_json = response.json()

    assert response_json["status"] == "unhealthy"
    assert response_json["details"]["song_service"]["status"] == "unhealthy"
    assert (
        response_json["details"]["song_service"]["message"]
        == "Mocked SongService initialization failed"
    )
    assert response_json["details"]["database"]["status"] == "healthy"
    assert response_json["details"]["auth_config"]["status"] == "healthy"


def test_health_check_unhealthy_auth_config(mocker):
    mocker.patch(
        "app.spotify_electron.health.health_controller.check_database_connection",
        return_value=mock_check_database_connection(),
    )
    mocker.patch(
        "app.spotify_electron.health.health_controller.check_song_service",
        return_value=mock_check_song_service(),
    )
    mocker.patch(
        "app.spotify_electron.health.health_controller.check_auth_config",
        return_value={"status": "unhealthy", "message": "Mocked Auth configuration failed"},
    )

    response = client.get("/health/")
    assert response.status_code == HTTP_503_SERVICE_UNAVAILABLE
    response_json = response.json()

    assert response_json["status"] == "unhealthy"
    assert response_json["details"]["auth_config"]["status"] == "unhealthy"
    assert (
        response_json["details"]["auth_config"]["message"]
        == "Mocked Auth configuration failed"
    )
    assert response_json["details"]["database"]["status"] == "healthy"
    assert response_json["details"]["song_service"]["status"] == "healthy"
