"""
Playlist controller for handling incoming HTTP Requests
"""

from typing import Annotated

from fastapi import APIRouter, Body, Query
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

import app.spotify_electron.playlist.playlist_service as playlist_service
import app.spotify_electron.utils.json_converter.json_converter_utils as json_converter_utils
from app.auth.auth_schema import (
    BadJWTTokenProvidedError,
    UserUnauthorizedError,
)
from app.auth.JWTBearer import Token
from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.exceptions.base_exceptions_schema import JsonEncodeError
from app.logging.logging_constants import LOGGING_PLAYLIST_CONTROLLER
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.playlist.playlist_schema import (
    PlaylistAlreadyExistsError,
    PlaylistBadNameError,
    PlaylistNotFoundError,
    PlaylistServiceError,
)
from app.spotify_electron.song.base_song_schema import (
    SongBadNameError,
    SongNotFoundError,
)

router = APIRouter(
    prefix="/playlists",
    tags=["Playlists"],
)

playlist_controller_logger = SpotifyElectronLogger(LOGGING_PLAYLIST_CONTROLLER).get_logger()


@router.get("/{name}")
def get_playlist(
    name: str,
    token: Token,
) -> Response:
    """Get playlist

    Args:
        name (str): playlist name
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        playlist = playlist_service.get_playlist(name)
        playlist_json = json_converter_utils.get_json_from_model(playlist)

        return Response(playlist_json, media_type="application/json", status_code=HTTP_200_OK)

    except PlaylistBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except PlaylistNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.playlistNotFound,
        )
    except JsonEncodeError:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, PlaylistServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.post("/")
def create_playlist(
    name: str,
    photo: str,
    description: str,
    token: Token,
    song_names: Annotated[list[str], Body(...)],
) -> Response:
    """Create playlist

    Args:
        name (str): playlist name
        photo (str): playlist photo
        description (str): playlist description
        song_names (list[str]): list of song names included in playlist.
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        playlist_service.create_playlist(
            name=name,
            photo=photo,
            description=description,
            song_names=song_names,
            token=token,
        )
        return Response(None, HTTP_201_CREATED)
    except BadJWTTokenProvidedError:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (PlaylistBadNameError, PlaylistAlreadyExistsError):
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except PlaylistNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.playlistNotFound,
        )
    except (Exception, PlaylistServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.put("/{name}")
def update_playlist(  # noqa: PLR0917
    name: str,
    photo: str,
    description: str,
    token: Token,
    song_names: Annotated[list[str], Body(...)],
    new_name: str | None = None,
) -> Response:
    """Update playlist

    Args:
        name (str): playlist name
        photo (str): playlist new photo
        description (str): playlist new description
        song_names (list[str], optional): playlist new song names. Defaults to Body(...).
        new_name (str | None, optional): playlist new name. Defaults to None.
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        playlist_service.update_playlist(name, new_name, photo, description, song_names, token)
        return Response(None, HTTP_204_NO_CONTENT)
    except BadJWTTokenProvidedError:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserUnauthorizedError:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.userUnauthorized,
        )
    except PlaylistBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except PlaylistNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.playlistNotFound,
        )
    except (Exception, PlaylistServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.delete("/{name}")
def delete_playlist(name: str) -> Response:
    """Delete playlsit

    Args:
        name (str): playlist name
    """
    try:
        playlist_service.delete_playlist(name)
        return Response(status_code=HTTP_202_ACCEPTED)
    except PlaylistBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except PlaylistNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.playlistNotFound,
        )
    except (Exception, PlaylistServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/")
def get_playlists(token: Token) -> Response:
    """Get all playlists"""
    try:
        playlists = playlist_service.get_all_playlist()
        playlist_json = json_converter_utils.get_json_with_iterable_field_from_model(
            playlists, "playlists"
        )

        return Response(playlist_json, media_type="application/json", status_code=HTTP_200_OK)
    except PlaylistBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except PlaylistNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.playlistNotFound,
        )
    except JsonEncodeError:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, PlaylistServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/selected/{names}")
def get_selected_playlists(names: str, token: Token) -> Response:
    """Get selected playlists

    Args:
        names (str): playlist names
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        playlists = playlist_service.get_selected_playlists(names.split(","))

        playlist_json = json_converter_utils.get_json_with_iterable_field_from_model(
            playlists, "playlists"
        )

        return Response(playlist_json, media_type="application/json", status_code=HTTP_200_OK)
    except PlaylistBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except PlaylistNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except JsonEncodeError:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, PlaylistServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.patch("/{name}/songs/")
def add_songs_to_playlist(name: str, song_names: list[str]) -> Response:
    """Add songs to playlist

    Args:
        name (str): playlist name
        song_names (list[str]): song names
    """
    try:
        playlist_service.add_songs_to_playlist(name, song_names)
        return Response(None, HTTP_204_NO_CONTENT)
    except PlaylistBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except PlaylistNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
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
    except (Exception, PlaylistServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.delete("/{name}/songs/")
def remove_songs_from_playlist(
    name: str, song_names: Annotated[list[str], Query(...)]
) -> Response:
    """Remove songs from playlist

    Args:
        name (str): playlist name
        song_names (list[str]): song names
    """
    try:
        playlist_service.remove_songs_from_playlist(name, song_names)
        return Response(None, HTTP_202_ACCEPTED)
    except PlaylistBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except PlaylistNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
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
    except (Exception, PlaylistServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )
