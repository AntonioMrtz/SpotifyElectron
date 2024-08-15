"""
Health controller for handling incoming HTTP Requests
"""

from fastapi import APIRouter
from fastapi.responses import Response
from starlette.status import HTTP_200_OK

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", summary="Health Check Endpoint")
def get_health() -> Response:
    """Validates if the app has launched correctly

    Returns
    -------
        Response 200 OK

    """
    return Response(status_code=HTTP_200_OK, content="OK", media_type="text/plain")
