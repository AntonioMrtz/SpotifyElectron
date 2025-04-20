"""Playlist controller for handling incoming HTTP Requests"""

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
async def get_playlist(
    name: str,
    token: Token,
) -> Response:
    """Get playlist

    Args:
        name: playlist name
        token: JWT info
    """
    try:
        playlist = await playlist_service.get_playlist(name)
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
async def create_playlist(
    name: str,
    photo: str,
    description: str,
    token: Token,
    song_names: Annotated[list[str], Body(...)],
) -> Response:
    """Create playlist

    Args:
        name: playlist name
        photo: playlist photo
        description: playlist description
        song_names: list of song names included in playlist.
        token: JWT info
    """
    try:
        await playlist_service.create_playlist(
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
async def update_playlist(  # noqa: PLR0917
    name: str,
    photo: str,
    description: str,
    token: Token,
    song_names: Annotated[list[str], Body(...)],
    new_name: str | None = None,
) -> Response:
    """Update playlist

    Args:
        name: playlist name
        photo: playlist new photo
        description: playlist new description
        song_names: playlist new song names. Defaults to Body(...).
        new_name: playlist new name. Defaults to None.
        token: JWT info
    """
    try:
        await playlist_service.update_playlist(
            name, new_name, photo, description, song_names, token
        )
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
async def delete_playlist(name: str) -> Response:
    """Delete playlsit

    Args:
        name: playlist name
    """
    try:
        await playlist_service.delete_playlist(name)
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
async def get_playlists(token: Token) -> Response:
    """Get all playlists"""
    try:
        playlists = await playlist_service.get_all_playlist()
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
async def get_selected_playlists(names: str, token: Token) -> Response:
    """Get selected playlists

    Args:
        names: playlist names
        token: JWT info
    """
    try:
        playlists = await playlist_service.get_selected_playlists(
            [name.strip() for name in names.split(",")]
        )

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
async def add_songs_to_playlist(name: str, song_names: list[str]) -> Response:
    """Add songs to playlist

    Args:
        name: playlist name
        song_names: song names
    """
    try:
        await playlist_service.add_songs_to_playlist(name, song_names)
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
async def remove_songs_from_playlist(
    name: str, song_names: Annotated[list[str], Query(...)]
) -> Response:
    """Remove songs from playlist

    Args:
        name: playlist name
        song_names: song names
    """
    try:
        await playlist_service.remove_songs_from_playlist(name, song_names)
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
