from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", summary="Health Check Endpoint")
def get_health():
    """Health endpoint allows us to determine if the app has launched correctly

    Returns
    -------
        Response 200 OK

    """
    return Response(status_code=200, content="OK", media_type="text/plain")
