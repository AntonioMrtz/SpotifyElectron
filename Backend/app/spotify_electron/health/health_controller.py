"""
Health controller for handling incoming HTTP Requests
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict
from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

from app.auth.auth_schema import AuthConfig
from app.database.DatabaseConnectionManager import DatabaseConnectionManager
from app.spotify_electron.song.providers.song_service_provider import SongServiceProvider
from app.logging.logging_schema import SpotifyElectronLogger
from app.logging.logging_constants import LOGGING_HEALTH

router = APIRouter(prefix="/health", tags=["health"])
logger = SpotifyElectronLogger(LOGGING_HEALTH).getLogger()

class HealthCheckResponse(BaseModel):
    status: str
    details: Dict[str, Dict[str, str]]

async def check_database_connection() -> Dict[str, str]:
    try:
        db_client = DatabaseConnectionManager.get_database_client()
        await db_client.admin.command('ping')
        return {"status": "healthy", "message": "Database connection is active"}
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {"status": "unhealthy", "message": f"Database connection failed: {str(e)}"}

def check_song_service() -> Dict[str, str]:
    try:
        service = SongServiceProvider.get_service()
        if service is None:
            return {"status": "unhealthy", "message": "SongService is not initialized"}
        return {"status": "healthy", "message": "SongService is properly initialized"}
    except Exception as e:
        logger.error(f"SongService health check failed: {str(e)}")
        return {"status": "unhealthy", "message": f"SongService check failed: {str(e)}"}

def check_auth_config() -> Dict[str, str]:
    try:
        if not all([
            hasattr(AuthConfig, 'SIGNING_SECRET_KEY') and AuthConfig.SIGNING_SECRET_KEY,
            hasattr(AuthConfig, 'VERTIFICATION_ALGORITHM') and AuthConfig.VERTIFICATION_ALGORITHM,
            hasattr(AuthConfig, 'ACCESS_TOKEN_EXPIRE_MINUTES') and AuthConfig.ACCESS_TOKEN_EXPIRE_MINUTES,
            hasattr(AuthConfig, 'DAYS_TO_EXPIRE_COOKIE') and AuthConfig.DAYS_TO_EXPIRE_COOKIE
        ]):
            return {
                "status": "unhealthy",
                "message": "Auth configuration is not fully initialized"
            }
        
        return {
            "status": "healthy",
            "message": "Auth configuration is properly initialized"
        }
    except Exception as e:
        logger.error(f"Auth configuration health check failed: {str(e)}")
        return {"status": "unhealthy", "message": f"Auth configuration check failed: {str(e)}"}

@router.get(
    "/",
    response_model=HealthCheckResponse,
    summary="Health Check Endpoint",
    description="Validates if the app and its critical components are functioning correctly"
)
async def get_health() -> JSONResponse:
    """Validates if the app has launched correctly and all critical components are healthy
    
    Returns
    -------
        JSONResponse with health status and details of each component
        200 OK if all components are healthy
        503 Service Unavailable if any component is unhealthy
    """
    db_health = await check_database_connection()
    service_health = check_song_service()
    auth_health = check_auth_config()
    
    health_details = {
        "database": db_health,
        "song_service": service_health,
        "auth_config": auth_health
    }
    
    is_healthy = all(check["status"] == "healthy" for check in health_details.values())
    
    response_data = {
        "status": "healthy" if is_healthy else "unhealthy",
        "details": health_details
    }
    
    status_code = HTTP_200_OK if is_healthy else HTTP_503_SERVICE_UNAVAILABLE
    
    if not is_healthy:
        logger.warning(f"Health check failed: {health_details}")
    
    return JSONResponse(
        content=response_data,
        status_code=status_code
    )
