from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import Response
import services.search_service as search_service
from typing import Annotated, Union



router = APIRouter(
    prefix="/search",
    tags=["search"],
)


@router.get("/",tags=["search"])
def get_search_nombre(nombre: str) -> Response:
    """ Devuelve los items con un nombre similar

    Parameters
    ----------
        Nombre (str) : parámetro de búsqueda por nombre

    Returns
    -------
        Response 200 OK
        Bad Request 400: "nombre" es vacío o nulo

    Raises
    -------
    """
    items = search_service.search_by_name(name=nombre)

    return Response(items, media_type="application/json", status_code=200)
