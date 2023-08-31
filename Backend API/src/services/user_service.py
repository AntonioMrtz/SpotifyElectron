from datetime import datetime
from database.Database import Database
import services.user_service as user_service
from model.User import User
from fastapi import HTTPException
from services.utils import checkValidParameterString

user_collection = Database().connection["usuario"]


def get_user(name: str) -> User:
    """ Returns user with name "name"

    Parameters
    ----------
        name (str): Users's name

    Raises
    -------
        400 : Bad Request
        404 : User not found

    Returns
    -------
        User object
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    user_data = user_collection.find_one({'name': name})

    if user_data is None:
        raise HTTPException(
            status_code=404, detail="El usuario con ese nombre no existe")

    date = user_data["register_date"][:-1]

    user = User(name=user_data["name"], photo=user_data["photo"], register_date=date, password=user_data["password"],
                playback_history=user_data["playback_history"], playlists=user_data["playlists"], saved_playlists=user_data["saved_playlists"])

    return user


def create_user(name: str, photo: str, password: str) -> None:
    """ Creates a user

    Parameters
    ----------
        name (str): Users's name
        photo (str): Url of users thumbnail
        password (str) : Password of users account

    Raises
    -------
        400 : Bad Request

    Returns
    -------
    """

    current_date = datetime.now()
    date_iso8601 = current_date.strftime('%Y-%m-%dT%H:%M:%S')

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result_user_exists = user_collection.find_one({'name': name})

    if result_user_exists:
        raise HTTPException(status_code=400, detail="La playlist ya existe")

    result = user_collection.insert_one(
        {'name': name, 'photo': photo if 'http' in photo else '', 'register_date': date_iso8601, 'password': password,'saved_playlists': [], 'playlists': [], 'playback_history': []})

    return True if result.acknowledged else False


def update_playlist(name: str, nuevo_nombre: str, photo: str, description: str, song_names: list) -> None:
    """ Updates a playlist with name, url of thumbnail and list of song names [ duplicates wont be added ]

    Parameters
    ----------
        name (str): Playlists's name
        nuevo_nombre (str) : New Playlist's name, if empty name is not being updated
        photo (str): Url of playlist thumbnail
        song_names (list<str>): List of song names of the playlist
        description (str): Playlists's description

    Raises
    -------
        400 : Bad Request
        404 : User Not Found

    Returns
    -------
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result_playlist_exists = playlistCollection.find_one({'name': name})

    if not result_playlist_exists:
        raise HTTPException(status_code=404, detail="La playlist no existe")

    if checkValidParameterString(nuevo_nombre):
        new_name = nuevo_nombre
        playlistCollection.update_one({'name': name}, {
            "$set": {'name': new_name, 'description': description, 'photo': photo if 'http' in photo else '', 'song_names': list(set(song_names))}})

    else:

        playlistCollection.update_one({'name': name}, {
            "$set": {'name': name, 'description': description, 'photo': photo if 'http' in photo else '', 'song_names': list(set(song_names))}})


def delete_user(name: str) -> None:
    """ Deletes a user by name

    Parameters
    ----------
        name (str): Users's name

    Raises
    -------
        400 : Bad Request
        404 : User Not Found

    Returns
    -------
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result = user_collection.delete_one({'name': name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="El usuario no existe")
