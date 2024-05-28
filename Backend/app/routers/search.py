import json

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response

from app.services import search_service

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
    items_dict = jsonable_encoder(items)
    items_json = json.dumps(items_dict)

    return Response(items_json, media_type="application/json", status_code=200)
