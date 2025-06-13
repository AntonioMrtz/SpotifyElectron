"""Health controller for handling incoming HTTP Requests"""

from fastapi import APIRouter
from fastapi.responses import Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_503_SERVICE_UNAVAILABLE,
)

from app.auth.auth_schema import AuthConfig, AuthServiceHealthCheckError
from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.database.database_schema import DatabasePingFailedError
from app.database.DatabaseConnectionManager import DatabaseConnectionManager
from app.spotify_electron.song.base_song_schema import SongServiceHealthCheckError
from app.spotify_electron.song.providers.song_service_provider import SongServiceProvider

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", summary="Health Check Endpoint")
async def get_health() -> Response:
    """Validates if the application has launched correctly by returning a health check response

    Response:
        HTTP 200 OK with "OK" content if all services are healthy.
        HTTP 503 Service Unavailable with specific error message if a particular
        service health check fails
        HTTP 500 Internal Server Error with generic error message for unexpected errors
    """
    try:
        await DatabaseConnectionManager.check_database_health()
        AuthConfig.check_auth_health()
        SongServiceProvider.check_song_service_health()
        return Response(status_code=HTTP_200_OK, content="OK", media_type="text/plain")
    except DatabasePingFailedError:
        return Response(
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            content=PropertiesMessagesManager.databaseUnhealthy,
        )
    except SongServiceHealthCheckError:
        return Response(
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            content=PropertiesMessagesManager.songServiceUnhealthy,
        )
    except AuthServiceHealthCheckError:
        return Response(
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            content=PropertiesMessagesManager.authServiceUnhealthy,
        )
    except Exception:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )
