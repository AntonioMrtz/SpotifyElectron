"""
Genre controller for handling incoming HTTP Requests
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

import app.spotify_electron.genre.genre_service as genre_service
from app.auth.auth_schema import TokenData
from app.auth.JWTBearer import JWTBearer
from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.logging.logging_constants import LOGGING_GENRE_CONTROLLER
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.genre.genre_schema import GenreServiceError

router = APIRouter(
    prefix="/genres",
    tags=["Genres"],
)

genre_controller_logger = SpotifyElectronLogger(LOGGING_GENRE_CONTROLLER).get_logger()


@router.get("/")
def get_genres(token: Annotated[TokenData, Depends(JWTBearer())]) -> Response:
    """Get all genres and their string representation"""
    try:
        genres = genre_service.get_genres()
        return Response(genres, media_type="application/json", status_code=HTTP_200_OK)

    except (GenreServiceError, Exception):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )
