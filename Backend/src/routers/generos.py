import services.genre_service as genre_service
from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(
    prefix="/generos",
    tags=["generos"],
)


@router.get("/")
def get_generos() -> Response:
    """Devuelve el enumerado Género

    Parameters
    ----------

    Returns
    -------
        Response 200 OK

    Raises
    -------
    """
    genres = genre_service.get_genres()

    return Response(genres, media_type="application/json", status_code=200)
