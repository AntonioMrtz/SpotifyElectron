import src.services.artist_service as artist_service
import src.services.user_service as user_service
import src.services.song_service as song_service
import src.services.playlist_service as playlist_service
from fastapi import HTTPException
from src.model.TokenData import TokenData
from src.model.UserType import User_Type
from src.services.utils import checkValidParameterString


services_map = {
    User_Type.USER: user_service,
    User_Type.ARTIST: artist_service,
}


MAX_NUMBER_PLAYBACK_HISTORY_SONGS = 5


def isArtistOrUser(user_name: str) -> User_Type or null:
    """Checks if the user_name is user or artists

    Parameters
    ----------
        user_name (str): Users's name

    Raises
    -------
        400 : Bad parameters
        404 : User not found

    Returns
    -------
        User_Type | null
    """

    if not checkValidParameterString(user_name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    if user_service.check_user_exists(user_name):
        return User_Type.USER

    elif artist_service.check_artists_exists(user_name):
        return User_Type.ARTIST

    else:
        raise HTTPException(status_code=404, detail="Usuario no existe")


def check_user_exists(user_name: str) -> bool:
    """Checks if the user or artists exists

    Parameters
    ----------
        user_name (str): Users's name

    Raises
    -------
        400 : Bad Request


    Returns
    -------
        Boolean
    """

    if not checkValidParameterString(user_name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result_artist_exists = artist_service.check_artists_exists(user_name)
    result_user_exists = user_service.check_user_exists(user_name)

    return result_user_exists or result_artist_exists


def add_playback_history(user_name: str, song: str, token: TokenData) -> None:
    """Updates the playback history of the user or artist

    Parameters
    ----------
        user_name (str): Users's name
        song (str) : Song that is going to be added to the playback history
        token (TokenData) : token with user data


    Raises
    -------
        400 : Bad Request
        401 : Unauthorized
        404 : User Not Found / Song not found

    Returns
    -------
    """

    if not checkValidParameterString(user_name) or not checkValidParameterString(song):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    user_service.check_jwt_is_user(token=token, user=user_name)

    if not check_user_exists(user_name=user_name):
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if not song_service.check_song_exists(song):
        raise HTTPException(status_code=404, detail="La canción no existe")

    user_type = isArtistOrUser(user_name)

    services_map[user_type].add_playback_history(
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
    -------
        400 : Bad Request
        401 : Unauthorized
        404 : User Not Found / Playlist not found

    Returns
    -------
    """

    if not checkValidParameterString(user_name) or not checkValidParameterString(
        playlist_name
    ):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    user_service.check_jwt_is_user(token=token, user=user_name)

    if not check_user_exists(user_name=user_name):
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if not playlist_service.check_playlist_exists(playlist_name):
        raise HTTPException(status_code=404, detail="La playlist no existe")

    user_type = isArtistOrUser(user_name)

    services_map[user_type].add_saved_playlist(
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
    -------
        400 : Bad Request
        401 : Unauthorized
        404 : User Not Found / Playlist not found

    Returns
    -------
    """

    if not checkValidParameterString(user_name) or not checkValidParameterString(
        playlist_name
    ):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    user_service.check_jwt_is_user(token=token, user=user_name)

    if not check_user_exists(user_name=user_name):
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if not playlist_service.check_playlist_exists(playlist_name):
        raise HTTPException(status_code=404, detail="La playlist no existe")

    user_type = isArtistOrUser(user_name)

    services_map[user_type].delete_saved_playlist(
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
    -------
        400 : Bad Request
        401 : Unauthorized
        404 : User Not Found / Playlist not found

    Returns
    -------
    """

    if not checkValidParameterString(user_name) or not checkValidParameterString(
        playlist_name
    ):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    user_service.check_jwt_is_user(token=token, user=user_name)

    if not playlist_service.check_playlist_exists(playlist_name):
        raise HTTPException(status_code=404, detail="La playlist no existe")

    if not check_user_exists(user_name=user_name):
        raise HTTPException(status_code=404, detail="El usuario no existe")

    user_type = isArtistOrUser(user_name)

    services_map[user_type].add_playlist_to_owner(
        user_name=user_name, playlist_name=playlist_name
    )


def delete_playlist_from_owner(playlist_name: str) -> None:
    """Deletes the playlist from the user that created it

    Parameters
    ----------
        playlist_name (str) : Playlist name

    Raises
    -------
        400 : Bad Request
        404 : User Not Found / Playlist not found

    Returns["owner"]
    -------
    """

    if not checkValidParameterString(playlist_name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    if not playlist_service.check_playlist_exists(playlist_name):
        raise HTTPException(status_code=404, detail="La playlist no existe")

    user_name = playlist_service.get_playlist(playlist_name).owner

    if not check_user_exists(user_name=user_name):
        raise HTTPException(status_code=404, detail="El usuario no existe")

    user_type = isArtistOrUser(user_name)

    services_map[user_type].delete_playlist_from_owner(
        user_name=user_name, playlist_name=playlist_name
    )
