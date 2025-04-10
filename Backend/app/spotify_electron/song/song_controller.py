"""
Song controller for handling incoming HTTP Requests
It uses the base_song_service for handling logic for different song architectures
"""

from fastapi import APIRouter, UploadFile
from fastapi.responses import Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

import app.spotify_electron.song.base_song_service as base_song_service
import app.spotify_electron.utils.json_converter.json_converter_utils as json_converter_utils
from app.auth.auth_schema import (
    BadJWTTokenProvidedError,
    UserUnauthorizedError,
)
from app.auth.JWTBearer import Token
from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.exceptions.base_exceptions_schema import JsonEncodeError
from app.spotify_electron.genre.genre_schema import Genre, GenreNotValidError
from app.spotify_electron.song.base_song_schema import (
    SongAlreadyExistsError,
    SongBadNameError,
    SongNotFoundError,
    SongServiceError,
)
from app.spotify_electron.song.providers.song_service_provider import get_song_service
from app.spotify_electron.user.user.user_schema import (
    UserBadNameError,
    UserNotFoundError,
)
from app.spotify_electron.utils.audio_management.audio_management_utils import (
    EncodingFileError,
)

router = APIRouter(
    prefix="/songs",
    tags=["Songs"],
)


@router.get("/{name}")
async def get_song(
    name: str,
    token: Token,
) -> Response:
    """Get song

    Args:
        name (str): song name
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        song = await get_song_service().get_song(name)
        song_json = json_converter_utils.get_json_from_model(song)

        return Response(song_json, media_type="application/json", status_code=HTTP_200_OK)
    except SongBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.songBadName,
        )
    except SongNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.songNotFound,
        )
    except JsonEncodeError:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, SongServiceError):
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
    token: Token,
) -> Response:
    """Create song

    Args:
        name (str): song name
        genre (Genre): genre
        photo (str): photo
        file (UploadFile): song file
        token (Annotated[TokenData, Depends): JWT info
    """
    read_file = await file.read()

    try:
        await get_song_service().create_song(name, genre, photo, read_file, token)
        return Response(None, HTTP_201_CREATED)
    except GenreNotValidError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.genreNotValid,
        )
    except UserBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except SongBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.songBadName,
        )
    except SongAlreadyExistsError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.songAlreadyExists,
        )
    except EncodingFileError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.songBadFile,
        )
    except BadJWTTokenProvidedError:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserUnauthorizedError:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.songCreateUnauthorizedUser,
        )
    except UserNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except (Exception, SongServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.delete("/{name}")
async def delete_song(name: str) -> Response:
    """Delete song

    Args:
        name (str): song name
    """
    try:
        await base_song_service.delete_song(name)

        return Response(None, HTTP_202_ACCEPTED)
    except SongBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.songBadName,
        )
    except UserNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except SongNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.songNotFound,
        )
    except (Exception, SongServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/metadata/{name}")
async def get_song_metadata(
    name: str,
    token: Token,
) -> Response:
    """Get song metadata

    Args:
        name (str): the song name
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        song = await base_song_service.get_song_metadata(name)
        song_json = json_converter_utils.get_json_from_model(song)
    except JsonEncodeError:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, SongServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )

    return Response(song_json, media_type="application/json", status_code=HTTP_200_OK)


@router.patch("/{name}/streams")
async def increase_song_streams(
    name: str,
    token: Token,
) -> Response:
    """Increase total streams of a song

    Args:
        name (str): song name
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        await base_song_service.increase_song_streams(name)
        return Response(None, HTTP_204_NO_CONTENT)
    except SongNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.songNotFound,
        )
    except (Exception, SongServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/genres/{genre}")
async def get_songs_by_genre(
    genre: Genre,
    token: Token,
) -> Response:
    """Get songs by genre

    Args:
        genre (Genre): the genre to match
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        songs = await base_song_service.get_songs_by_genre(genre)
        songs_json = json_converter_utils.get_json_with_iterable_field_from_model(
            songs, "songs"
        )
        return Response(songs_json, media_type="application/json", status_code=HTTP_200_OK)
    except GenreNotValidError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.genreNotValid,
        )
    except JsonEncodeError:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, SongServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )
