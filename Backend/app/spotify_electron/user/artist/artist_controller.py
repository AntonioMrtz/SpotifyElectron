"""
Artist controller for handling incoming HTTP Requests
"""

import json
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

import app.spotify_electron.user.artist.artist_service as artist_service
import app.spotify_electron.utils.json_converter.json_converter_utils as json_converter_utils
from app.auth.auth_schema import (
    BadJWTTokenProvidedException,
    TokenData,
    UserUnauthorizedException,
)
from app.auth.JWTBearer import JWTBearer
from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.exceptions.base_exceptions_schema import JsonEncodeException
from app.spotify_electron.song.base_song_schema import SongBadNameException
from app.spotify_electron.user.artist.artist_schema import (
    ArtistBadNameException,
    ArtistNotFoundException,
    ArtistServiceException,
)
from app.spotify_electron.user.base_user_schema import BaseUserAlreadyExistsException

router = APIRouter(
    prefix="/artists",
    tags=["Artists"],
)


@router.get("/{name}")
def get_artist(
    name: str,
    token: Annotated[TokenData, Depends(JWTBearer())],
) -> Response:
    """Get artist by name

    Args:
        name (str): artist name
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        artist = artist_service.get_artist(name)
        artist_json = json_converter_utils.get_json_from_model(artist)

        return Response(artist_json, media_type="application/json", status_code=HTTP_200_OK)

    except ArtistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.artistBadName,
        )
    except ArtistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.artistNotFound,
        )
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, ArtistServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.post("/")
def create_artist(
    name: str,
    photo: str,
    password: str,
) -> Response:
    """Create artist

    Args:
        name (str): artist name
        photo (str): artist photo
        password (str): artist password
    """
    try:
        artist_service.create_artist(name, photo, password)
        return Response(None, HTTP_201_CREATED)
    except (ArtistBadNameException, BaseUserAlreadyExistsException):
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.artistBadName,
        )
    except (Exception, ArtistServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/")
def get_artists(token: Annotated[TokenData, Depends(JWTBearer())]) -> Response:
    """Get all artists"""
    try:
        artists = artist_service.get_all_artists()
        artists_dict = {}
        artists_dict["artists"] = jsonable_encoder(artists)

        artists_json = json.dumps(artists_dict)

        return Response(artists_json, media_type="application/json", status_code=HTTP_200_OK)
    except ArtistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.artistBadName,
        )
    except ArtistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.artistNotFound,
        )
    except UserUnauthorizedException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.userUnauthorized,
        )
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, ArtistServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/{name}/songs")
def get_artist_songs(
    name: str,
    token: Annotated[TokenData, Depends(JWTBearer())],
) -> Response:
    """Get artist songs"""
    try:
        artist_songs = artist_service.get_artists_songs(name)
        artist_songs_json = json_converter_utils.get_json_from_model(artist_songs)

        return Response(
            artist_songs_json, media_type="application/json", status_code=HTTP_200_OK
        )
    except SongBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.songBadName,
        )
    except UserUnauthorizedException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.userUnauthorized,
        )
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, ArtistServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )
