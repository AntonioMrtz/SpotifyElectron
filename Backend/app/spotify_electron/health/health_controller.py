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

    This endpoint can be used to verify that the server is running and responding to requests.
    It checks both database connectivity and song service availability.

    Returns:
        Response: HTTP 200 OK if all services are healthy,
                 HTTP 500 if services are unhealthy but reachable,
                 HTTP 503 if specific service errors occur.
    """
    try:
        if (
            await DatabaseConnectionManager.check_database_health()
            and SongServiceProvider.check_service_health()
            and AuthConfig.check_auth_health()
        ):
            return Response(status_code=HTTP_200_OK, content="OK", media_type="text/plain")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content="Health check failed",
            media_type="text/plain",
        )
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
