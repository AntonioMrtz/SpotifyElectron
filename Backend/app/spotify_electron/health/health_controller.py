"""
Health controller for handling incoming HTTP Requests
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

from app.auth.auth_schema import AuthConfig
from app.database.database_schema import DatabasePingFailedException
from app.database.DatabaseConnectionManager import DatabaseConnectionManager
from app.logging.logging_constants import LOGGING_HEALTH
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.health.health_schema import HealthCheckResponse
from app.spotify_electron.song.providers.song_service_provider import SongServiceProvider

router = APIRouter(prefix="/health", tags=["health"])
logger = SpotifyElectronLogger(LOGGING_HEALTH).getLogger()


def check_database_connection() -> dict[str, str]:
    """Validates ping to database

    Returns:
        dict[str, str]: Dictionary with status and explanatory message
    """
    try:
        if DatabaseConnectionManager.ping_database():
            return {"status": "healthy", "message": "Database connection is active"}
    except DatabasePingFailedException:
        logger.exception(DatabasePingFailedException.ERROR)
    else:
        return {"status": "unhealthy", "message": DatabasePingFailedException.ERROR}


def check_song_service() -> dict[str, str]:
    """Validates if SongServiceProvider is inited

    Returns:
        dict[str, str]: Dictionary with status and explanatory message
    """
    try:
        service = SongServiceProvider.get_song_service()
    except Exception as exception:
        logger.exception("SongServiceProvider health check failed")
        return {
            "status": "unhealthy",
            "message": f"SongServiceProvider check failed: {str(exception)}",
        }
    else:
        if service is None:
            return {"status": "unhealthy", "message": "SongServiceProvider is not initialized"}
        return {"status": "healthy", "message": "SongServiceProvider is properly initialized"}


def check_auth_config() -> dict[str, str]:
    """Validates if auth configurations are set

    Returns:
        dict[str, str]: Dictionary with status and explanatory message
    """
    try:
        if not all(
            [
                hasattr(AuthConfig, "VERTIFICATION_ALGORITHM")
                and AuthConfig.VERTIFICATION_ALGORITHM,
                hasattr(AuthConfig, "ACCESS_TOKEN_EXPIRE_MINUTES")
                and AuthConfig.ACCESS_TOKEN_EXPIRE_MINUTES,
                hasattr(AuthConfig, "DAYS_TO_EXPIRE_COOKIE")
                and AuthConfig.DAYS_TO_EXPIRE_COOKIE,
            ]
        ):
            return {
                "status": "unhealthy",
                "message": "Auth configuration is not fully initialized",
            }
    except Exception:
        logger.exception("Auth configuration health check failed")
        return {
            "status": "unhealthy",
            "message": "Auth configuration check failed",
        }
    else:
        return {"status": "healthy", "message": "Auth configuration is properly initialized"}


@router.get(
    "/",
    response_model=HealthCheckResponse,
    summary="Health Check Endpoint",
    description="Validates if the app and its critical components are functioning correctly",
)
async def get_health() -> JSONResponse:
    """Validates if the app has launched correctly and all critical components are healthy

    Returns:
        JSONResponse: health status with details of each component and status code
    """
    db_health = check_database_connection()
    service_health = check_song_service()
    auth_health = check_auth_config()

    health_details = {
        "database": db_health,
        "song_service": service_health,
        "auth_config": auth_health,
    }

    is_healthy = all(check["status"] == "healthy" for check in health_details.values())

    response_data = {
        "status": "healthy" if is_healthy else "unhealthy",
        "details": health_details,
    }

    status_code = HTTP_200_OK if is_healthy else HTTP_503_SERVICE_UNAVAILABLE

    if not is_healthy:
        logger.warning(f"Health check failed: {health_details}")

    return JSONResponse(content=response_data, status_code=status_code)
