from datetime import datetime
from database.Database import Database
from model.Artist import Artist
from fastapi import HTTPException
from services.utils import checkValidParameterString
from services.all_users_service import check_user_exists
import bcrypt


artist_collection = Database().connection["artista"]
user_collection = Database().connection["usuario"]


def get_artist(name: str) -> Artist:
    """ Returns artist with name "name"

    Parameters
    ----------
        name (str): Artist's name

    Raises
    -------
        400 : Bad Request
        404 : Artist not found

    Returns
    -------
        Artist
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    artist_data = artist_collection.find_one({'name': name})

    if artist_data is None:
        raise HTTPException(
            status_code=404, detail="El artista con ese nombre no existe")

    date = artist_data["register_date"][:-1]

    artist = Artist(name=artist_data["name"], photo=artist_data["photo"], register_date=date, password=artist_data["password"],
                    playback_history=artist_data["playback_history"], playlists=artist_data["playlists"], saved_playlists=artist_data["saved_playlists"], uploaded_songs=artist_data["uploaded_songs"])

    return artist


def create_artist(name: str, photo: str, password: str) -> None:
    """ Creates an artist

    Parameters
    ----------
        name (str): Artist's name
        photo (str): Url of artists thumbnail
        password (str) : Password of artists account

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
        raise HTTPException(status_code=400, detail="El artista ya existe")

    utf8_password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(utf8_password, bcrypt.gensalt())

    result = artist_collection.insert_one(
        {'name': name, 'photo': photo if 'http' in photo else '', 'register_date': date_iso8601, 'password': hashed_password, 'saved_playlists': [], 'playlists': [], 'playback_history': [], 'uploaded_songs': []})

    return True if result.acknowledged else False


def update_artist(name: str, photo: str, playlists: list, saved_playlists: list, playback_history: list, uploaded_songs: list) -> None:
    """ Updates a artist , duplicated playlists and songs wont be added

    Parameters
    ----------
        name (str): Artists's name
        photo (str): Url of artist thumbnail
        playlists (list) : artists playlists
        playlists (list) : others artists playlists saved by artist with name "name"
        playback_history (list) : song names of playback history of the artist


    Raises
    -------
        400 : Bad Request
        404 : Artist Not Found

    Returns
    -------
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result_artist_exists = artist_collection.find_one({'name': name})

    if not result_artist_exists:
        raise HTTPException(status_code=404, detail="El artista no existe")

    result = artist_collection.update_one({'name': name},
                                          {"$set": {'photo': photo if 'http' in photo else '', 'saved_playlists': list(set(saved_playlists)), 'playlists': list(set(playlists)), 'playback_history': list(set(playback_history)),    'uploaded_songs': list(set(uploaded_songs))}})


def delete_artist(name: str) -> None:
    """ Deletes a artist by name

    Parameters
    ----------
        name (str): Artists's name

    Raises
    -------
        400 : Bad Request
        404 : Artist Not Found

    Returns
    -------
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result = artist_collection.delete_one({'name': name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="El artista no existe")
