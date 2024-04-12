from datetime import datetime
from sys import modules
from typing import List

import app.services.all_users_service as all_users_service
import app.services.dto_service as dto_service
from app.database.Database import Database
from app.model.Playlist import Playlist
from app.model.TokenData import TokenData
from app.services.song_services.song_service_provider import get_song_service
from app.services.utils import checkValidParameterString
from fastapi import HTTPException

if "pytest" in modules:
    playlist_collection = Database().connection["test.playlist"]

else:
    playlist_collection = Database().connection["playlist"]

song_service = get_song_service()


def check_jwt_user_is_playlist_owner(token: TokenData, owner: str) -> bool:
    """Check if the user is the playlist owner

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
            status_code=401, detail="El usuario no es el creador de la canción"
        )


def check_playlist_exists(name: str) -> bool:
    """Check if the song exists or not

    Parameters
    ----------
        name (str): Playlist's name

    Raises
    -------

    Returns
    -------
        Boolean
    """
    return True if playlist_collection.find_one({"name": name}) else False


def get_playlist(name: str) -> Playlist:
    """Returns a Playlist with his songs"

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

    playlist_data = playlist_collection.find_one({"name": name})

    if playlist_data is None:
        raise HTTPException(
            status_code=404, detail="La playlist con ese nombre no existe"
        )

    playlist_songs = []

    [
        playlist_songs.append(dto_service.get_song(song_name).name)
        for song_name in playlist_data["song_names"]
    ]

    date = playlist_data["upload_date"][:-1]

    playlist = Playlist(
        name,
        playlist_data["photo"],
        playlist_data["description"],
        date,
        playlist_data["owner"],
        playlist_songs,
    )

    return playlist


def create_playlist(
    name: str, photo: str, description: str, song_names: list, token: TokenData
) -> None:
    """Create a playlist with name, url of thumbnail and list of song names

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
    fecha_iso8601 = fecha_actual.strftime("%Y-%m-%dT%H:%M:%S")

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result_playlist_exists = playlist_collection.find_one({"name": name})

    if result_playlist_exists:
        raise HTTPException(status_code=400, detail="La playlist ya existe")

    if not all_users_service.check_user_exists(owner):
        raise HTTPException(status_code=404, detail="El usuario no existe")

    result = playlist_collection.insert_one(
        {
            "name": name,
            "photo": photo if "http" in photo else "",
            "upload_date": fecha_iso8601,
            "description": description,
            "owner": owner,
            "song_names": song_names,
        }
    )

    all_users_service.add_playlist_to_owner(
        user_name=owner, playlist_name=name, token=token
    )

    return True if result.acknowledged else False


def update_playlist(
    name: str,
    nuevo_nombre: str,
    photo: str,
    description: str,
    song_names: list,
    token: TokenData,
) -> None:
    """Updates a playlist with name, url of thumbnail and list of song names [ duplicates wont be added ]

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

    result_playlist_exists = playlist_collection.find_one({"name": name})

    if not result_playlist_exists:
        raise HTTPException(status_code=404, detail="La playlist no existe")

    check_jwt_user_is_playlist_owner(token=token, owner=result_playlist_exists["owner"])

    if checkValidParameterString(nuevo_nombre):
        new_name = nuevo_nombre
        playlist_collection.update_one(
            {"name": name},
            {
                "$set": {
                    "name": new_name,
                    "description": description,
                    "photo": photo if "http" in photo else "",
                    "song_names": list(set(song_names)),
                }
            },
        )

    else:
        playlist_collection.update_one(
            {"name": name},
            {
                "$set": {
                    "name": name,
                    "description": description,
                    "photo": photo if "http" in photo else "",
                    "song_names": list(set(song_names)),
                }
            },
        )


def delete_playlist(name: str) -> None:
    """Deletes a playlist by name

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
        all_users_service.delete_playlist_from_owner(playlist_name=name)

        result = playlist_collection.delete_one({"name": name})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="La playlist no existe")

    except:
        result = playlist_collection.delete_one({"name": name})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="La playlist no existe")


def get_all_playlist() -> list:
    """Returns all playlists in a DTO object"

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
    playlists_files = playlist_collection.find()

    for playlist_file in playlists_files:
        playlists.append(get_playlist(playlist_file["name"]))

    return playlists


def get_selected_playlists(playlist_names: list) -> list:
    """Returns the selected playlists DTO object"

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
    playlists_files = playlist_collection.find(filter_contained_playlist_names)

    for playlist_file in playlists_files:
        response_playlists.append(get_playlist(playlist_file["name"]))

    return response_playlists


def search_by_name(name: str) -> List[Playlist]:
    """Retrieve the playlists than match the name

    Args:
        name (str): the name to match

    Returns:
        List[Playlist]: a list with the playlists that match the name
    """

    playlist_names_response = playlist_collection.find(
        {"name": {"$regex": name, "$options": "i"}}, {"_id": 0, "name": 1}
    )

    playlist_names = []

    [playlist_names.append(playlist["name"]) for playlist in playlist_names_response]

    playlists = get_selected_playlists(playlist_names)

    return playlists
