from datetime import datetime
from database.Database import Database
from model.User import User
from fastapi import HTTPException
from services.utils import checkValidParameterString
from model.TokenData import TokenData
from sys import modules
import bcrypt
import json


if "pytest" in modules:

    user_collection = Database().connection["test.usuario"]
    artist_collection = Database().connection["test.artista"]

else:

    user_collection = Database().connection["usuario"]
    artist_collection = Database().connection["artista"]


def check_jwt_is_user(token: TokenData, user: str) -> bool:
    """ Check if user is the same as token user

    Parameters
    ----------
        token (TokenData) : token with user data
        user (str): user name

    Raises
    -------
        Unauthorized 401


    Returns
    -------
        Boolean
    """

    if token.username == user:
        return True
    else:
        raise HTTPException(
            status_code=401, detail="El usuario está modificando otro usuario")


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

    if check_user_exists(name):
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    utf8_password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(utf8_password, bcrypt.gensalt())

    result = user_collection.insert_one(
        {'name': name, 'photo': photo if 'http' in photo else '', 'register_date': date_iso8601, 'password': hashed_password, 'saved_playlists': [], 'playlists': [], 'playback_history': []})

    return True if result.acknowledged else False


def update_user(name: str, photo: str, playlists: list, saved_playlists: list, playback_history: list, token: TokenData) -> None:
    """ Updates a user , duplicated playlists and songs wont be added

    Parameters
    ----------
        name (str): Users's name
        photo (str): Url of user thumbnail
        playlists (list) : users playlists
        playlists (list) : others users playlists saved by user with name "name"
        playback_history (list) : song names of playback history of the user
        token (TokenData) : token data from the user

    Raises
    -------
        400 : Bad Request
        404 : User Not Found

    Returns
    -------
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result_user_exists = user_collection.find_one({'name': name})

    check_jwt_is_user(token, name)

    if not result_user_exists:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    result = user_collection.update_one({'name': name},
                                        {"$set": {'photo': photo if 'http' in photo else '', 'saved_playlists': list(set(saved_playlists)), 'playlists': list(set(playlists)), 'playback_history': list(set(playback_history))}})


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


def get_users(names: list) -> list:
    """ Returns a list of Users that match "names" list of names

    Parameters
    ----------
        names (list): List of user Names

    Raises
    -------
            400 : Bad Request
            404 : User not found

    Returns
    -------
        List<User>

    """

    users: list = []

    for user_name in names:

        users.append(get_user(user_name))

    return users


def search_by_name(name: str) -> list:
    """ Returns a list of Users that contains "name" in their names

    Parameters
    ----------
        name (str) : name to search by

    Raises
    -------
            400 : Bad Request
            404 : User not found

    Returns
    -------
        List<Json>
    """

    users_names_response = user_collection.find(
        {'name': {'$regex': name, '$options': 'i'}}, {"_id": 0, "name": 1})

    user_names = []

    [user_names.append(user["name"]) for user in users_names_response]

    users = get_users(user_names)

    users_json_list = []

    [users_json_list.append(user.get_json()) for user in users]

    return users_json_list


# * AUX METHODs

def check_user_exists(user_name: str) -> bool:
    """ Checks if the user exists

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

    return True if result_user_exists else False


def add_playback_history(user_name: str, song: str, MAX_NUMBER_PLAYBACK_HISTORY_SONGS: int):
    user_data = user_collection.find_one({'name': user_name})

    playback_history = user_data["playback_history"]

    if len(playback_history) == MAX_NUMBER_PLAYBACK_HISTORY_SONGS:
        playback_history.pop(0)

    playback_history.append(song)

    result = user_collection.update_one({'name': user_name},
                                        {"$set": {'playback_history': playback_history}})


def add_saved_playlist(user_name: str, playlist_name: str):
    user_data = user_collection.find_one({'name': user_name})

    saved_playlists = user_data["saved_playlists"]

    saved_playlists.append(playlist_name)

    result = user_collection.update_one({'name': user_name},
                                        {"$set": {'saved_playlists': list(set(saved_playlists))}})


def delete_saved_playlist(user_name: str, playlist_name: str):
    user_data = user_collection.find_one({'name': user_name})

    saved_playlists = user_data["saved_playlists"]

    if playlist_name in saved_playlists:

        saved_playlists.remove(playlist_name)

        result = user_collection.update_one({'name': user_name},
                                            {"$set": {'saved_playlists': saved_playlists}})


def add_playlist_to_owner(user_name: str, playlist_name: str) -> None:

    user_data = user_collection.find_one({'name': user_name})

    playlists = user_data["playlists"]

    playlists.append(playlist_name)

    result = user_collection.update_one({'name': user_name},
                                        {"$set": {'playlists': list(set(playlists))}})


def delete_playlist_from_owner(user_name: str, playlist_name: str) -> None:

    user_data = user_collection.find_one({'name': user_name})

    playlists = user_data["playlists"]

    if playlist_name in playlists:

        playlists.remove(playlist_name)

        result = user_collection.update_one({'name': user_name},
                                            {"$set": {'playlists': playlists}})
