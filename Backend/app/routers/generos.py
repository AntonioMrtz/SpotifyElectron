import app.services.genre_service as genre_service
import app.services.http_encode_service as http_encode_service

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
    genres_json = http_encode_service.get_json(genres)

    return Response(genres_json, media_type="application/json", status_code=200)
