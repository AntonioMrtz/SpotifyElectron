"""Artist controller for handling incoming HTTP Requests"""

import json

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

import app.spotify_electron.user.artist.artist_service as artist_service
import app.spotify_electron.utils.json_converter.json_converter_utils as json_converter_utils
from app.auth.auth_schema import (
    BadJWTTokenProvidedError,
    UserUnauthorizedError,
)
from app.auth.JWTBearer import Token
from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.exceptions.base_exceptions_schema import JsonEncodeError
from app.spotify_electron.song.base_song_schema import SongBadNameError
from app.spotify_electron.user.artist.artist_schema import (
    ArtistBadNameError,
    ArtistNotFoundError,
    ArtistServiceError,
)
from app.spotify_electron.user.base_user_schema import BaseUserAlreadyExistsError

router = APIRouter(
    prefix="/artists",
    tags=["Artists"],
)


@router.get("/{name}")
async def get_artist(
    name: str,
    token: Token,
) -> Response:
    """Get artist by name

    Args:
        name: artist name
        token: JWT info
    """
    try:
        artist = await artist_service.get_artist(name)
        artist_json = json_converter_utils.get_json_from_model(artist)

        return Response(artist_json, media_type="application/json", status_code=HTTP_200_OK)

    except ArtistBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.artistBadName,
        )
    except ArtistNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.artistNotFound,
        )
    except BadJWTTokenProvidedError:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JsonEncodeError:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, ArtistServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.post("/")
async def create_artist(
    name: str,
    photo: str,
    password: str,
) -> Response:
    """Create artist

    Args:
        name: artist name
        photo: artist photo
        password: artist password
    """
    try:
        await artist_service.create_artist(name, photo, password)
        return Response(None, HTTP_201_CREATED)
    except (ArtistBadNameError, BaseUserAlreadyExistsError):
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.artistBadName,
        )
    except (Exception, ArtistServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/")
async def get_artists(token: Token) -> Response:
    """Get all artists"""
    try:
        artists = await artist_service.get_all_artists()
        artists_dict = {}
        artists_dict["artists"] = jsonable_encoder(artists)

        artists_json = json.dumps(artists_dict)

        return Response(artists_json, media_type="application/json", status_code=HTTP_200_OK)
    except ArtistBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.artistBadName,
        )
    except ArtistNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.artistNotFound,
        )
    except UserUnauthorizedError:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.userUnauthorized,
        )
    except BadJWTTokenProvidedError:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JsonEncodeError:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, ArtistServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/{name}/songs")
async def get_artist_songs(
    name: str,
    token: Token,
) -> Response:
    """Get artist songs"""
    try:
        artist_songs = await artist_service.get_artists_songs(name)
        artist_songs_json = json_converter_utils.get_json_from_model(artist_songs)

        return Response(
            artist_songs_json, media_type="application/json", status_code=HTTP_200_OK
        )
    except SongBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.songBadName,
        )
    except UserUnauthorizedError:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.userUnauthorized,
        )
    except BadJWTTokenProvidedError:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JsonEncodeError:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, ArtistServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )
