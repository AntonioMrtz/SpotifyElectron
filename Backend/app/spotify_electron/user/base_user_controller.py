"""
User controller for handling incoming HTTP Requests
It uses the base_user_service for handling logic for different user types
"""

from typing import Annotated

from fastapi import APIRouter, Depends
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

import app.spotify_electron.user.base_user_service as base_user_service
import app.spotify_electron.user.user.user_service as user_service
import app.spotify_electron.utils.json_converter.json_converter_utils as json_converter_utils
from app.auth.auth_schema import (
    BadJWTTokenProvidedException,
    TokenData,
    UserUnauthorizedException,
)
from app.auth.JWTBearer import JWTBearer
from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.exceptions.base_exceptions_schema import JsonEncodeException
from app.spotify_electron.playlist.playlist_schema import (
    PlaylistBadNameException,
    PlaylistNotFoundException,
)
from app.spotify_electron.song.base_song_schema import (
    SongBadNameException,
    SongNotFoundException,
)
from app.spotify_electron.user.base_user_schema import (
    BaseUserAlreadyExistsException,
    BaseUserBadNameException,
    BaseUserNotFoundException,
    BaseUserServiceException,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/whoami")
def get_who_am_i(token: Annotated[TokenData, Depends(JWTBearer())]) -> Response:
    """Returns token info from JWT

    Args:
        token (TokenData): the jwt token. Defaults to None.
    """
    try:
        jwt_token_json = json_converter_utils.get_json_from_model(token)

        return Response(jwt_token_json, media_type="application/json", status_code=200)
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/{name}")
def get_user(name: str, token: Annotated[TokenData, Depends(JWTBearer())]) -> Response:
    """Get user by name

    Args:
        name (str): user name
    """
    try:
        user = base_user_service.get_user(name)
        user_json = json_converter_utils.get_json_from_model(user)

        return Response(user_json, media_type="application/json", status_code=HTTP_200_OK)

    except BaseUserBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except BaseUserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, BaseUserServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.post("/")
def create_user(name: str, photo: str, password: str) -> Response:
    """Create user

    Args:
        name (str): user name
        photo (str): user photo
        password (str): user password
    """
    try:
        user_service.create_user(name, photo, password)
        return Response(None, HTTP_201_CREATED)
    except (BaseUserBadNameException, BaseUserAlreadyExistsException):
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except BaseUserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except (Exception, BaseUserServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.delete("/{name}")
def delete_user(name: str) -> Response:
    """Delete user

    Args:
        name (str): user name
    """
    try:
        base_user_service.delete_user(name)
        return Response(status_code=HTTP_202_ACCEPTED)
    except BaseUserBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except BaseUserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except (Exception, BaseUserServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.patch("/{name}/playback_history")
def patch_playback_history(
    name: str, song_name: str, token: Annotated[TokenData, Depends(JWTBearer())]
) -> Response:
    """Add song to playback history

    Args:
        name (str): user name
        song_name (str): song name
    """
    try:
        base_user_service.add_playback_history(
            user_name=name, song_name=song_name, token=token
        )
        return Response(None, HTTP_204_NO_CONTENT)
    except BaseUserBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except SongBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.songBadName,
        )
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
    except BaseUserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except SongNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.songNotFound,
        )
    except (Exception, BaseUserServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.patch("/{name}/saved_playlists")
def patch_saved_playlists(
    name: str, playlist_name: str, token: Annotated[TokenData, Depends(JWTBearer())]
) -> Response:
    """Add playlist to saved list

    Args:
        name (str): user name
        playlist_name (str): saved playlist
    """
    try:
        base_user_service.add_saved_playlist(name, playlist_name, token=token)
        return Response(None, HTTP_204_NO_CONTENT)
    except BaseUserBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except UserUnauthorizedException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.userUnauthorized,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.playlistNotFound,
        )
    except BaseUserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (Exception, BaseUserServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.delete("/{name}/saved_playlists")
def delete_saved_playlists(
    name: str, playlist_name: str, token: Annotated[TokenData, Depends(JWTBearer())]
) -> Response:
    """Delete playlist from saved list of user

    Args:
        name (str): user name
        playlist_name (str): playlist name
    """
    try:
        base_user_service.delete_saved_playlist(name, playlist_name, token=token)
        return Response(None, HTTP_202_ACCEPTED)
    except BaseUserBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except PlaylistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except UserUnauthorizedException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.userUnauthorized,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.playlistNotFound,
        )
    except BaseUserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (Exception, BaseUserServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/{name}/relevant_playlists")
def get_user_relevant_playlists(
    name: str, token: Annotated[TokenData, Depends(JWTBearer())]
) -> Response:
    """Get relevant playlists for user

    Args:
        name (str): user name
    """
    try:
        playlists = base_user_service.get_user_relevant_playlists(name)
        playlists_json = json_converter_utils.get_json_from_model(playlists)
        return Response(playlists_json, media_type="application/json", status_code=HTTP_200_OK)
    except BaseUserBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except BaseUserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, BaseUserServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/{name}/playlists")
def get_user_playlists(
    name: str, token: Annotated[TokenData, Depends(JWTBearer())]
) -> Response:
    """Get playlists created by the user

    Args:
        name (str): user name
    """
    try:
        playlists = base_user_service.get_user_playlists(name)
        playlists_json = json_converter_utils.get_json_from_model(playlists)
        return Response(playlists_json, media_type="application/json", status_code=HTTP_200_OK)
    except BaseUserBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except BaseUserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, BaseUserServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/{name}/playlist_names")
def get_user_playlists_names(
    name: str, token: Annotated[TokenData, Depends(JWTBearer())]
) -> Response:
    """Get playlist names created by user

    Args:
        name (str): user name
    """
    try:
        playlist_names = base_user_service.get_user_playlist_names(name)
        playlist_names_json = json_converter_utils.get_json_from_model(playlist_names)
        return Response(
            playlist_names_json, media_type="application/json", status_code=HTTP_200_OK
        )
    except BaseUserBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except BaseUserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, BaseUserServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/{name}/playback_history")
def get_user_playback_history(
    name: str, token: Annotated[TokenData, Depends(JWTBearer())]
) -> Response:
    """Get user song playback history

    Args:
        name (str): user name
    """
    try:
        playback_history = base_user_service.get_user_playback_history(name)
        playback_history_json = json_converter_utils.get_json_from_model(playback_history)
        return Response(
            playback_history_json, media_type="application/json", status_code=HTTP_200_OK
        )
    except BaseUserBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except BaseUserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, BaseUserServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )
