from datetime import datetime
from database.Database import Database
from services.song_service import get_song
from services.all_users_service import add_playlist_to_owner, delete_playlist_from_owner, check_user_exists
from model.Playlist import Playlist
from model.Song import Song
from model.TokenData import TokenData
from fastapi import HTTPException
from services.utils import checkValidParameterString
from sys import modules
import services.dto_service as dto_service
import json


if "pytest" in modules:

    playlistCollection = Database().connection["test.playlist"]

else:

    playlistCollection = Database().connection["playlist"]


def check_jwt_user_is_playlist_owner(token: TokenData, owner: str) -> bool:
    """ Check if the user is the playlist owner

    Parameters
    ----------
        token (TokenData): token with the user data
        owner (str) : owner of the playlist

    Raises
    -------
        Unauthorized 401

    Returns
    -------
        Boolean
    """

    if token.username == owner:
        return True
    else:
        raise HTTPException(
            status_code=401, detail="El usuario no es el creador de la canción")


def get_playlist(name: str) -> Playlist:
    """ Returns a Playlist with his songs"

    Parameters
    ----------
        name (str): Playlists's name

    Raises
    -------
        400 : Bad Request
        404 : Playlist not found

    Returns
    -------
        Playlist object
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    playlist_data = playlistCollection.find_one({'name': name})

    if playlist_data is None:
        raise HTTPException(
            status_code=404, detail="La playlist con ese nombre no existe")

    playlist_songs = []

    [playlist_songs.append(get_song(song_name))
        for song_name in playlist_data["song_names"]]

    # [print(song.name) for song in playlist_songs]

    date = playlist_data["upload_date"][:-1]

    playlist = Playlist(
        name, playlist_data["photo"], playlist_data["description"], date, playlist_data["owner"], playlist_songs)

    return playlist


def create_playlist(name: str, photo: str, description: str, song_names: list, token: TokenData) -> None:
    """ Create a playlist with name, url of thumbnail and list of song names

    Parameters
    ----------
        name (str): Playlists's name
        photo (str): Url of playlist thumbnail
        description (str): Playlists's description
        song_names (list<str>): List of song names of the playlist
        token (TokenData) : token with user data

    Raises
    -------
        400 : Bad Request

    Returns
    -------
    """
    owner = token.username

    fecha_actual = datetime.now()
    fecha_iso8601 = fecha_actual.strftime('%Y-%m-%dT%H:%M:%S')

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    songs = dto_service.get_songs(song_names)
    result_playlist_exists = playlistCollection.find_one({'name': name})

    if result_playlist_exists:
        raise HTTPException(status_code=400, detail="La playlist ya existe")

    if not check_user_exists(owner):
        raise HTTPException(status_code=404, detail="El usuario no existe")

    result = playlistCollection.insert_one(
        {'name': name, 'photo': photo if 'http' in photo else '', 'upload_date': fecha_iso8601, 'description': description, 'owner': owner, 'song_names': song_names})

    add_playlist_to_owner(user_name=owner, playlist_name=name, token=token)

    return True if result.acknowledged else False


def update_playlist(name: str, nuevo_nombre: str, photo: str, description: str, song_names: list, token: TokenData) -> None:
    """ Updates a playlist with name, url of thumbnail and list of song names [ duplicates wont be added ]

    Parameters
    ----------
        name (str): Playlists's name
        nuevo_nombre (str) : New Playlist's name, if empty name is not being updated
        photo (str): Url of playlist thumbnail
        description (str): Playlists's description
        song_names (list<str>): List of song names of the playlist
        token (TokenData) : token with user data


    Raises
    -------
        400 : Bad Request
        404 : Playlist Not Found

    Returns
    -------
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result_playlist_exists = playlistCollection.find_one({'name': name})

    if not result_playlist_exists:
        raise HTTPException(status_code=404, detail="La playlist no existe")

    check_jwt_user_is_playlist_owner(
        token=token, owner=result_playlist_exists["owner"])

    if checkValidParameterString(nuevo_nombre):
        new_name = nuevo_nombre
        playlistCollection.update_one({'name': name}, {
            "$set": {'name': new_name, 'description': description, 'photo': photo if 'http' in photo else '', 'song_names': list(set(song_names))}})

    else:

        playlistCollection.update_one({'name': name}, {
            "$set": {'name': name, 'description': description, 'photo': photo if 'http' in photo else '', 'song_names': list(set(song_names))}})


def delete_playlist(name: str) -> None:
    """ Deletes a playlist by name

    Parameters
    ----------
        name (str): Playlists's name

    Raises
    -------
        400 : Bad Request
        404 : Playlist Not Found

    Returns
    -------
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    try:
        delete_playlist_from_owner(playlist_name=name)

        result = playlistCollection.delete_one({'name': name})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404, detail="La playlist no existe")

    except:
        result = playlistCollection.delete_one({'name': name})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404, detail="La playlist no existe")


def get_all_playlist() -> list:
    """ Returns all playlists in a DTO object"

    Parameters
    ----------

    Raises
    -------
        400 : Bad Request
        404 : Playlist Not Found

    Returns
    -------
        List<PlaylistDTO>
    """

    playlists: list = []
    playlists_files = playlistCollection.find()

    for playlist_file in playlists_files:
        playlists.append(dto_service.get_playlist(playlist_file["name"]))

    return playlists


def get_selected_playlists(playlist_names: list) -> list:
    """ Returns the selected playlists DTO object"

    Parameters
    ----------
    playlist_names (list<str>) : the names of the playlists

    Raises
    -------
    400

    Returns
    -------
        List<PlaylistDTO>
    """

    filter_contained_playlist_names = {"name": {"$in": playlist_names}}

    response_playlists = []
    playlists_files = playlistCollection.find(filter_contained_playlist_names)

    for playlist_file in playlists_files:
        response_playlists.append(
            dto_service.get_playlist(playlist_file["name"]))

    return response_playlists


def search_by_name(name: str) -> json:
    """ Returns a list of Playlists that contains "name" in their names

    Parameters
    ----------
        name (str): name to filter by

    Raises
    -------
            400 : Bad Request
            404 : Playlist not found

    Returns
    -------
        List<PlaylistDTO>
    """

    playlist_names_response = playlistCollection.find(
        {'name': {'$regex': name, '$options': 'i'}}, {"_id": 0, "name": 1})

    playlist_names = []

    [playlist_names.append(playlist["name"])
     for playlist in playlist_names_response]

    playlists = get_selected_playlists(playlist_names)

    playlists_json_list = []

    [playlists_json_list.append(playlist.get_json()) for playlist in playlists]

    return playlists_json_list
