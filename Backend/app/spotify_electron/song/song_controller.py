"""
Song controller for handling incoming HTTP Requests
It uses the base_song_service for handling logic for different song architectures
"""

from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

import app.spotify_electron.song.base_song_service as base_song_service
import app.spotify_electron.utils.json_converter.json_converter_utils as json_converter_utils
from app.auth.auth_schema import BadJWTTokenProvidedException, TokenData
from app.auth.JWTBearer import JWTBearer
from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.exceptions.base_exceptions_schema import JsonEncodeException
from app.spotify_electron.genre.genre_schema import Genre, GenreNotValidException
from app.spotify_electron.song.base_song_schema import (
    SongAlreadyExistsException,
    SongBadNameException,
    SongNotFoundException,
    SongServiceException,
    SongUnAuthorizedException,
)
from app.spotify_electron.song.providers.song_service_provider import get_song_service
from app.spotify_electron.user.user.user_schema import (
    UserBadNameException,
    UserNotFoundException,
)
from app.spotify_electron.utils.audio_management.audio_management_utils import (
    EncodingFileException,
)

router = APIRouter(
    prefix="/songs",
    tags=["Songs"],
)


@router.get("/{name}")
def get_song(
    name: str,
    token: Annotated[TokenData | None, Depends(JWTBearer())],
) -> Response:
    """Get song

    Args:
        name (str): song name
    """
    try:
        song = get_song_service().get_song(name)
        song_json = json_converter_utils.get_json_from_model(song)

        return Response(song_json, media_type="application/json", status_code=HTTP_200_OK)
    except SongBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.songBadName,
        )
    except SongNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.songNotFound,
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, SongServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.post("/")
async def create_song(
    name: str,
    genre: Genre,
    photo: str,
    file: UploadFile,
    token: Annotated[TokenData | None, Depends(JWTBearer())],
) -> Response:
    """Create song

    Args:
        name (str): song name
        genre (Genre): genre
        photo (str): photo
        file (UploadFile): song file
    """
    readFile = await file.read()

    try:
        await get_song_service().create_song(name, genre, photo, readFile, token)
        return Response(None, HTTP_201_CREATED)
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except GenreNotValidException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.genreNotValid,
        )
    except UserBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except SongBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.songBadName,
        )
    except SongAlreadyExistsException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.songAlreadyExists,
        )
    except UserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except EncodingFileException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.songBadFile,
        )
    except SongUnAuthorizedException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.songCreateUnauthorizedUser,
        )
    except (Exception, SongServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.delete("/{name}")
def delete_song(name: str) -> Response:
    """Delete song

    Args:
        name (str): song name
    """
    try:
        base_song_service.delete_song(name)

        return Response(None, HTTP_202_ACCEPTED)
    except SongBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.songBadName,
        )
    except UserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except SongNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.songNotFound,
        )
    except (Exception, SongServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/metadata/{name}")
def get_song_metadata(
    name: str,
    token: Annotated[TokenData | None, Depends(JWTBearer())],
) -> Response:
    """Get song metadata

    Args:
        name (str): the song name
    """
    try:
        song = base_song_service.get_song_metadata(name)
        song_json = json_converter_utils.get_json_from_model(song)
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, SongServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )

    return Response(song_json, media_type="application/json", status_code=HTTP_200_OK)


@router.patch("/{name}/streams")
def increase_song_streams(
    name: str,
    token: Annotated[TokenData | None, Depends(JWTBearer())],
) -> Response:
    """Increase total streams of a song

    Args:
        name (str): song name
    """
    try:
        base_song_service.increase_song_streams(name)
        return Response(None, HTTP_204_NO_CONTENT)
    except SongNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.songNotFound,
        )
    except (Exception, SongServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/genres/{genre}")
def get_songs_by_genre(
    genre: Genre,
    token: Annotated[TokenData | None, Depends(JWTBearer())],
) -> Response:
    """Get songs by genre

    Args:
        genre (Genre): the genre to match
    """
    try:
        songs = base_song_service.get_songs_by_genre(genre)
        songs_json = json_converter_utils.get_json_with_iterable_field_from_model(
            songs, "songs"
        )
        return Response(songs_json, media_type="application/json", status_code=HTTP_200_OK)
    except GenreNotValidException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.genreNotValid,
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, SongServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )
