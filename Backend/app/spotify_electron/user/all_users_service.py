from typing import Annotated, Any

from fastapi import HTTPException

import app.services.song_services.song_service_provider as song_service_provider
import app.spotify_electron.playlist.playlist_service as playlist_service
import app.spotify_electron.user.artist.artist_service as artist_service
import app.spotify_electron.user.user_service as user_service
from app.logging.logging_constants import LOGGING_ALL_USERS_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.security.security_schema import TokenData
from app.spotify_electron.user.user_schema import User, UserType
from app.spotify_electron.utils.validation.utils import validate_parameter

all_users_service_logger = SpotifyElectronLogger(LOGGING_ALL_USERS_SERVICE).getLogger()


# TODO not hardcoded
MAX_NUMBER_PLAYBACK_HISTORY_SONGS = 5

services_map = {
    UserType.USER: user_service,
    UserType.ARTIST: artist_service,
}


def get_user_type(user_name: str) -> UserType | None:
    """Checks if the user_name is user or artists

    Parameters
    ----------
        user_name (str): Users's name

    Raises
    ------
        400 : Bad parameters
        404 : User not found

    Returns
    -------
        UserTypes | null

    """
    if not validate_parameter(user_name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    if user_service.check_user_exists(user_name):
        return UserType.USER

    if artist_service.check_artists_exists(user_name):
        return UserType.ARTIST

    raise HTTPException(status_code=404, detail="Usuario no existe")


def check_user_exists(user_name: str) -> bool:
    """Checks if the user or artists exists

    Parameters
    ----------
        user_name (str): Users's name

    Raises
    ------
        400 : Bad Request


    Returns
    -------
        Boolean

    """
    if not validate_parameter(user_name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result_artist_exists = artist_service.check_artists_exists(user_name)
    result_user_exists = user_service.check_user_exists(user_name)

    return result_user_exists or result_artist_exists


def get_user_service(user_name: str) -> Annotated[Any, "ModuleType"]:
    """Returns the user service according to the user role

    Returns:
        ModuleType: the user service
    """
    user_type = get_user_type(user_name)
    if user_type not in services_map:
        all_users_service_logger.warning(
            f"User {user_name} doesn't have a valid user type, using {UserType.USER} type instead"
        )
        return services_map[UserType.USER]
    return services_map[user_type]


def get_user(user_name: str) -> User:
    """Returns the user

    Args:
        user_name (str): the user name

    Returns:
        User: the user
    """
    return get_user_service(user_name).get_user(user_name)


def add_playback_history(user_name: str, song: str, token: TokenData) -> None:
    """Updates the playback history of the user or artist

    Parameters
    ----------
        user_name (str): Users's name
        song (str) : Song that is going to be added to the playback history
        token (TokenData) : token with user data


    Raises
    ------
        400 : Bad Request
        401 : Unauthorized
        404 : User Not Found / Song not found

    Returns
    -------

    """
    if not validate_parameter(user_name) or not validate_parameter(song):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    user_service.check_jwt_is_user(token=token, user=user_name)

    if not check_user_exists(user_name=user_name):
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if not song_service_provider.song_service.check_song_exists(song):
        raise HTTPException(status_code=404, detail="La canción no existe")

    get_user_service(user_name).add_playback_history(
        user_name=user_name,
        song=song,
        MAX_NUMBER_PLAYBACK_HISTORY_SONGS=MAX_NUMBER_PLAYBACK_HISTORY_SONGS,
    )


def add_saved_playlist(user_name: str, playlist_name: str, token: TokenData) -> None:
    """Updates the saved playlist of the user

    Parameters
    ----------
        user_name (str): Users's name
        playlist_name (str) : Playlist thats going to be added to saved
                              playlist of the user
        token (TokenData) : token with user data


    Raises
    ------
        400 : Bad Request
        401 : Unauthorized
        404 : User Not Found / Playlist not found

    Returns
    -------

    """
    if not validate_parameter(user_name) or not validate_parameter(playlist_name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    user_service.check_jwt_is_user(token=token, user=user_name)

    if not check_user_exists(user_name=user_name):
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if not playlist_service.check_playlist_exists(playlist_name):
        raise HTTPException(status_code=404, detail="La playlist no existe")

    get_user_service(user_name).add_saved_playlist(
        user_name=user_name, playlist_name=playlist_name
    )


def delete_saved_playlist(user_name: str, playlist_name: str, token: TokenData) -> None:
    """Updates the saved playlist of the user

    Parameters
    ----------
        user_name (str): Users's name
        playlist_name (str) : Playlist thats going to be \
                              deleted to saved playlist of the user
        token (TokenData) : token with user data

    Raises
    ------
        400 : Bad Request
        401 : Unauthorized
        404 : User Not Found / Playlist not found

    Returns
    -------

    """
    if not validate_parameter(user_name) or not validate_parameter(playlist_name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    user_service.check_jwt_is_user(token=token, user=user_name)

    if not check_user_exists(user_name=user_name):
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if not playlist_service.check_playlist_exists(playlist_name):
        raise HTTPException(status_code=404, detail="La playlist no existe")

    get_user_service(user_name).delete_saved_playlist(
        user_name=user_name, playlist_name=playlist_name
    )


def add_playlist_to_owner(user_name: str, playlist_name: str, token: TokenData) -> None:
    """Adds the playlist to the user that created it

    Parameters
    ----------
        user_name (str): Users's name
        playlist_name (str) : Playlist name
        token (TokenData) : token with user data

    Raises
    ------
        400 : Bad Request
        401 : Unauthorized
        404 : User Not Found / Playlist not found

    Returns
    -------

    """
    if not validate_parameter(user_name) or not validate_parameter(playlist_name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    user_service.check_jwt_is_user(token=token, user=user_name)

    if not playlist_service.check_playlist_exists(playlist_name):
        raise HTTPException(status_code=404, detail="La playlist no existe")

    if not check_user_exists(user_name=user_name):
        raise HTTPException(status_code=404, detail="El usuario no existe")

    get_user_service(user_name).add_playlist_to_owner(
        user_name=user_name, playlist_name=playlist_name
    )


def delete_playlist_from_owner(playlist_name: str) -> None:
    """Deletes the playlist from the user that created it

    Parameters
    ----------
        playlist_name (str) : Playlist name

    Raises
    ------
        400 : Bad Request
        404 : User Not Found / Playlist not found

    Returns["owner"]
    -------

    """
    if not validate_parameter(playlist_name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    if not playlist_service.check_playlist_exists(playlist_name):
        raise HTTPException(status_code=404, detail="La playlist no existe")

    user_name = playlist_service.get_playlist(playlist_name).owner

    if not check_user_exists(user_name=user_name):
        raise HTTPException(status_code=404, detail="El usuario no existe")

    get_user_service(user_name).delete_playlist_from_owner(
        user_name=user_name, playlist_name=playlist_name
    )


def update_playlist_name(old_playlist_name: str, new_playlist_name: str) -> None:
    if not validate_parameter(old_playlist_name) or not validate_parameter(
        new_playlist_name
    ):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    for service in services_map.values():
        service.update_playlist_name(
            old_playlist_name=old_playlist_name, new_playlist_name=new_playlist_name
        )
