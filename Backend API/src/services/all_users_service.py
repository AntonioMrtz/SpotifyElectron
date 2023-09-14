from fastapi import HTTPException
from services.utils import checkValidParameterString
from database.Database import Database
from services.song_service import check_song_exists
from enum import Enum


user_collection = Database().connection["usuario"]
artist_collection = Database().connection["artista"]

MAX_NUMBER_PLAYBACK_HISTORY_SONGS = 5


class User_Type(Enum):
    ARTIST = "Artist"
    USER = "User"


def isArtistOrUser(user_name: str) -> User_Type or null:
    """ Checks if the user_name is user or artists

    Parameters
    ----------
        user_name (str): Users's name

    Raises
    -------

    Returns
    -------
        User_Type | null
    """

    if user_collection.find_one({'name': user_name}):
        return User_Type.USER

    elif artist_collection.find_one({'name': user_name}):
        return User_Type.ARTIST

    else:
        return null


def check_user_exists(user_name: str) -> bool:
    """ Checks if the user or artists exists

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

    result_user_exists = user_collection.find_one({'name': user_name})
    result_artist_exists = artist_collection.find_one({'name': user_name})

    return result_user_exists or result_artist_exists


def add_playback_history(user_name: str, song: str) -> None:
    """ Updates the playback history of the user or artist

    Parameters
    ----------
        user_name (str): Users's name
        song (str) : Song that is going to be added to the playback history


    Raises
    -------
        400 : Bad Request
        404 : User Not Found / Song not found

    Returns
    -------
    """

    if not checkValidParameterString(user_name) or not checkValidParameterString(song):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    if not check_user_exists(user_name=user_name):
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if not check_song_exists(song):
        raise HTTPException(status_code=404, detail="La canción no existe")

    user_type = isArtistOrUser(user_name)

    if user_type == User_Type.ARTIST:

        artist_data = artist_collection.find_one({'name': user_name})

        playback_history = artist_data["playback_history"]

        if len(playback_history) == MAX_NUMBER_PLAYBACK_HISTORY_SONGS:
            playback_history.pop(0)

        playback_history.append(song)

        result = artist_collection.update_one({'name': user_name},
                                              {"$set": {'playback_history': playback_history}})

    if user_type == User_Type.USER:

        user_data = user_collection.find_one({'name': user_name})

        playback_history = user_data["playback_history"]

        if len(playback_history) == MAX_NUMBER_PLAYBACK_HISTORY_SONGS:
            playback_history.pop(0)

        playback_history.append(song)

        result = user_collection.update_one({'name': user_name},
                                            {"$set": {'playback_history': playback_history}})
