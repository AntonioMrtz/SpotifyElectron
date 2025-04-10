"""
User controller for handling incoming HTTP Requests
It uses the base_user_service for handling logic for different user types
"""

from fastapi import APIRouter
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

import app.spotify_electron.user.base_user_service as base_user_service
import app.spotify_electron.user.user.user_service as user_service
import app.spotify_electron.utils.json_converter.json_converter_utils as json_converter_utils
from app.auth.auth_schema import (
    BadJWTTokenProvidedError,
    UserUnauthorizedError,
)
from app.auth.JWTBearer import Token
from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.exceptions.base_exceptions_schema import JsonEncodeError
from app.spotify_electron.playlist.playlist_schema import (
    PlaylistBadNameError,
    PlaylistNotFoundError,
)
from app.spotify_electron.song.base_song_schema import (
    SongBadNameError,
    SongNotFoundError,
)
from app.spotify_electron.user.artist.artist_schema import ArtistAlreadyExistsError
from app.spotify_electron.user.base_user_schema import (
    BaseUserAlreadyExistsError,
    BaseUserBadNameError,
    BaseUserNotFoundError,
    BaseUserServiceError,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/whoami")
def get_who_am_i(token: Token) -> Response:
    """Returns token info from JWT

    Args:
        token (TokenData): the jwt token. Defaults to None.
    """
    try:
        jwt_token_json = json_converter_utils.get_json_from_model(token)

        return Response(jwt_token_json, media_type="application/json", status_code=200)
    except BadJWTTokenProvidedError:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/{name}")
async def get_user(name: str, token: Token) -> Response:
    """Get user by name

    Args:
        name (str): user name
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        user = await base_user_service.get_user(name)
        user_json = json_converter_utils.get_json_from_model(user)

        return Response(user_json, media_type="application/json", status_code=HTTP_200_OK)

    except BaseUserBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except BaseUserNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
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
    except (Exception, BaseUserServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.post("/")
async def create_user(name: str, photo: str, password: str) -> Response:
    """Create user

    Args:
        name (str): user name
        photo (str): user photo
        password (str): user password
    """
    try:
        await user_service.create_user(name, photo, password)
        return Response(None, HTTP_201_CREATED)
    except (BaseUserBadNameError, BaseUserAlreadyExistsError):
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except (Exception, BaseUserServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.delete("/{name}")
async def delete_user(name: str) -> Response:
    """Delete user

    Args:
        name (str): user name
    """
    try:
        await base_user_service.delete_user(name)
        return Response(status_code=HTTP_202_ACCEPTED)
    except BaseUserBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except BaseUserNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except (Exception, BaseUserServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.patch("/{name}/playback_history")
async def patch_playback_history(name: str, song_name: str, token: Token) -> Response:
    """Add song to playback history

    Args:
        name (str): user name
        song_name (str): song name
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        await base_user_service.add_playback_history(
            user_name=name, song_name=song_name, token=token
        )
        return Response(None, HTTP_204_NO_CONTENT)
    except BaseUserBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except SongBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.songBadName,
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
            content=PropertiesMessagesManager.userUnauthorized,
        )
    except BaseUserNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except SongNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.songNotFound,
        )
    except (Exception, BaseUserServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.patch("/{name}/saved_playlists")
async def patch_saved_playlists(name: str, playlist_name: str, token: Token) -> Response:
    """Add playlist to saved list

    Args:
        name (str): user name
        playlist_name (str): saved playlist
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        await base_user_service.add_saved_playlist(name, playlist_name, token=token)
        return Response(None, HTTP_204_NO_CONTENT)
    except BaseUserBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except UserUnauthorizedError:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.userUnauthorized,
        )
    except PlaylistNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.playlistNotFound,
        )
    except BaseUserNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except BadJWTTokenProvidedError:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (Exception, BaseUserServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.delete("/{name}/saved_playlists")
async def delete_saved_playlists(name: str, playlist_name: str, token: Token) -> Response:
    """Delete playlist from saved list of user

    Args:
        name (str): user name
        playlist_name (str): playlist name
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        await base_user_service.delete_saved_playlist(name, playlist_name, token=token)
        return Response(None, HTTP_202_ACCEPTED)
    except BaseUserBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except PlaylistBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.playlistBadName,
        )
    except UserUnauthorizedError:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.userUnauthorized,
        )
    except PlaylistNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.playlistNotFound,
        )
    except BaseUserNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except BadJWTTokenProvidedError:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content=PropertiesMessagesManager.tokenInvalidCredentials,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (Exception, BaseUserServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/{name}/relevant_playlists")
async def get_user_relevant_playlists(name: str, token: Token) -> Response:
    """Get relevant playlists for user

    Args:
        name (str): user name
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        playlists = await base_user_service.get_user_relevant_playlists(name)
        playlists_json = json_converter_utils.get_json_from_model(playlists)
        return Response(playlists_json, media_type="application/json", status_code=HTTP_200_OK)
    except BaseUserBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except BaseUserNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except JsonEncodeError:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, BaseUserServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/{name}/playlists")
async def get_user_playlists(name: str, token: Token) -> Response:
    """Get playlists created by the user

    Args:
        name (str): user name
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        playlists = await base_user_service.get_user_playlists(name)
        playlists_json = json_converter_utils.get_json_from_model(playlists)
        return Response(playlists_json, media_type="application/json", status_code=HTTP_200_OK)
    except BaseUserBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except BaseUserNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except JsonEncodeError:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, BaseUserServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/{name}/playlist_names")
async def get_user_playlists_names(name: str, token: Token) -> Response:
    """Get playlist names created by user

    Args:
        name (str): user name
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        playlist_names = await base_user_service.get_user_playlist_names(name)
        playlist_names_json = json_converter_utils.get_json_from_model(playlist_names)
        return Response(
            playlist_names_json, media_type="application/json", status_code=HTTP_200_OK
        )
    except BaseUserBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except BaseUserNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except JsonEncodeError:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, BaseUserServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/{name}/playback_history")
async def get_user_playback_history(name: str, token: Token) -> Response:
    """Get user song playback history

    Args:
        name (str): user name
        token (Annotated[TokenData, Depends): JWT info
    """
    try:
        playback_history = await base_user_service.get_user_playback_history(name)
        playback_history_json = json_converter_utils.get_json_from_model(playback_history)
        return Response(
            playback_history_json, media_type="application/json", status_code=HTTP_200_OK
        )
    except BaseUserBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except BaseUserNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except JsonEncodeError:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, BaseUserServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.patch("/{name}/promote")
async def promote_user_to_artist(name: str, token: Token) -> Response:
    """Promote user to artist

    Args:
        name (str): user name
        token (Token): JWT info
    """
    try:
        await user_service.promote_user_to_artist(name, token)
        return Response(status_code=HTTP_204_NO_CONTENT)
    except ArtistAlreadyExistsError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.artistAlreadyExists,
        )
    except BaseUserBadNameError:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.userBadName,
        )
    except BaseUserNotFoundError:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except UserUnauthorizedError:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.userUnauthorized,
        )
    except (Exception, BaseUserServiceError):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )
