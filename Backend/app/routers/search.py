import app.services.http_encode_service as http_encode_service
import app.services.search_service as search_service
from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(
    prefix="/search",
    tags=["search"],
)


@router.get("/", tags=["search"])
def get_search_nombre(nombre: str) -> Response:
    """Search for items that partially match name

    Args:
        nombre (str): name to matcg

    Returns:
        Response: the response including a json with all the items
    """
    items = search_service.search_by_name(name=nombre)
    items_json = http_encode_service.get_json(items)

    return Response(items_json, media_type="application/json", status_code=200)
