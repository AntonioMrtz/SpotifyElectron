"""
Playlist controller for handling incoming HTTP Requests
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends
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

import app.spotify_electron.playlist.playlist_service as playlist_service
import app.spotify_electron.utils.json_converter.json_converter_utils as json_converter_utils
from app.auth.JWTBearer import JWTBearer
from app.auth.security_schema import (
    BadJWTTokenProvidedException,
    TokenData,
    UserUnauthorizedException,
)
from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.exceptions.base_exceptions_schema import JsonEncodeException
from app.logging.logging_constants import LOGGING_PLAYLIST_CONTROLLER
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.playlist.playlist_schema import (
    PlaylistAlreadyExistsException,
    PlaylistBadNameException,
    PlaylistNotFoundException,
    PlaylistServiceException,
)

router = APIRouter(
    prefix="/playlists",
    tags=["Playlists"],
)

playlist_controller_logger = SpotifyElectronLogger(LOGGING_PLAYLIST_CONTROLLER).getLogger()


@router.get("/{name}")
def get_playlist(
    name: str,
    token: Annotated[TokenData, Depends(JWTBearer())],
) -> Response:
    """Get playlsit

    Args:
        name (str): playlist name
    """
    try:
        playlist = playlist_service.get_playlist(name)
        playlist_json = json_converter_utils.get_json_from_model(playlist)

        return Response(playlist_json, media_type="application/json", status_code=HTTP_200_OK)

    except PlaylistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.playlistNotFound,
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, PlaylistServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.post("/")
def create_playlist(
    name: str,
    photo: str,
    description: str,
    token: Annotated[TokenData, Depends(JWTBearer())],
    song_names: list[str] = Body(...),
) -> Response:
    """Create playlist

    Args:
        name (str): playlist name
        photo (str): playlist photo
        description (str): playlist description
        song_names (list[str]): list of song names included in playlist.
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
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (PlaylistBadNameException, PlaylistAlreadyExistsException):
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.playlistNotFound,
        )
    except (Exception, PlaylistServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.put("/{name}")
def update_playlist(  # noqa: PLR0913
    name: str,
    photo: str,
    description: str,
    token: Annotated[TokenData, Depends(JWTBearer())],
    song_names: list[str] = Body(...),
    new_name: str | None = None,
) -> Response:
    """Update playlist

    Args:
        photo (str): playlist new photo
        description (str): playlist new description
        song_names (list[str], optional): playlist new song names. Defaults to Body(...).
        new_name (str | None, optional): playlist new name. Defaults to None.
        authorization (Annotated[str  |  None, Header, optional): jwt token. Defaults to None.
    """
    try:
        playlist_service.update_playlist(name, new_name, photo, description, song_names, token)
        return Response(None, HTTP_204_NO_CONTENT)
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserUnauthorizedException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.userUnauthorized,
        )
    except PlaylistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.playlistNotFound,
        )
    except (Exception, PlaylistServiceException):
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
    except PlaylistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.playlistNotFound,
        )
    except (Exception, PlaylistServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/")
def get_playlists(token: Annotated[TokenData, Depends(JWTBearer())]) -> Response:
    """Return all playlists"""
    try:
        playlists = playlist_service.get_all_playlist()
        playlist_json = json_converter_utils.get_json_with_iterable_field_from_model(
            playlists, "playlists"
        )

        return Response(playlist_json, media_type="application/json", status_code=HTTP_200_OK)
    except PlaylistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.playlistNotFound,
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, PlaylistServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/selected/{names}")
def get_selected_playlists(
    names: str, token: Annotated[TokenData, Depends(JWTBearer())]
) -> Response:
    """Get selected playlists

    Args:
        names (str): playlist names
    """
    try:
        playlists = playlist_service.get_selected_playlists(names.split(","))

        playlist_json = json_converter_utils.get_json_with_iterable_field_from_model(
            playlists, "playlists"
        )

        return Response(playlist_json, media_type="application/json", status_code=HTTP_200_OK)
    except PlaylistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, PlaylistServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )
