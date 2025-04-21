"""Health controller for handling incoming HTTP Requests"""

from fastapi import APIRouter
from fastapi.responses import Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_503_SERVICE_UNAVAILABLE,
)

from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.database.database_schema import DatabasePingFailedError
from app.database.DatabaseConnectionManager import DatabaseConnectionManager

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", summary="Health Check Endpoint")
def get_health() -> Response:
    """Validates if the application has launched correctly by returning a health check response

    This endpoint can be used to verify that the server is running and responding to requests.

    Returns
        Response 200 OK
    """
    try:
        if DatabaseConnectionManager.check_database_health():
            return Response(status_code=HTTP_200_OK, content="OK", media_type="text/plain")
    except DatabasePingFailedError:
        return Response(
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            content=PropertiesMessagesManager.databaseUnhealthy,
        )
    else:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.databaseUnhealthy,
        )
