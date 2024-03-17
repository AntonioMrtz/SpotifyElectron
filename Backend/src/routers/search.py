import services.search_service as search_service
from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(
    prefix="/search",
    tags=["search"],
)


@router.get("/", tags=["search"])
def get_search_nombre(nombre: str) -> Response:
    """Devuelve los items con un nombre similar

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
