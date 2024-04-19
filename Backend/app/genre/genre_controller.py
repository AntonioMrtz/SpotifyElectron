from fastapi import APIRouter
from fastapi.responses import Response
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

import app.genre.genre_service as genre_service
from app.genre.genre_schema import GenreServiceException

router = APIRouter(
    prefix="/genres",
    tags=["Genres"],
)


@router.get("/")
def get_genres() -> Response:
    """Get all genres and their string representation"""
    try:
        genres = genre_service.get_genres()
    except (GenreServiceException, Exception):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(genres, media_type="application/json", status_code=HTTP_200_OK)
