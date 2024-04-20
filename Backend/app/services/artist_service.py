from datetime import datetime
from sys import modules

from fastapi import HTTPException

import app.security.security_service as security_service
from app.database.Database import Database
from app.model.Artist import Artist
from app.security.security_schema import TokenData
from app.services.song_services.song_service_provider import get_song_service
from app.services.utils import checkValidParameterString

if "pytest" in modules:
    artist_collection = Database.get_instance().connection["test.artista"]

else:
    artist_collection = Database.get_instance().connection["artista"]

song_service = get_song_service()


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

    result_artist_exists = artist_collection.find_one({"name": user_name})

    return bool(result_artist_exists)


def check_artists_exists(artist_name: str) -> bool:
    """Checks if the user or artists exists

    Parameters
    ----------
        artist_name (str): Artists's name

    Raises
    -------
        400 : Bad Request


    Returns
    -------
        Boolean
    """

    if not checkValidParameterString(artist_name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    return bool(artist_collection.find_one({"name": artist_name}))


def check_jwt_artist_is_artist(token: TokenData, artist: str) -> bool:
    """Check if the user is the song artist

    Parameters
    ----------
        token (TokenData): token with the user data
        artist (str) : artist

    Raises
    -------
        401

    Returns
    -------
        Boolean
    """

    if token.username == artist:
        return True

    raise HTTPException(
        status_code=401, detail="El usuario no es el creador de la canción"
    )


def add_song_artist(artist_name: str, song_name: str):
    """Updates the uploaded songs of the artist adding "song_name"

    Parameters
    ----------
        artist_name (str): Artists's name
        song_name (str) : Song that is going to be added to the uploaded songs of the artist


    Raises
    -------
        400 : Bad Request
        404 : Artist Not Found / Song not found

    Returns
    -------
    """

    if not checkValidParameterString(artist_name) or not checkValidParameterString(
        song_name
    ):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    if not check_artists_exists(artist_name=artist_name):
        raise HTTPException(status_code=404, detail="El artista no existe")

    artist_collection.update_one(
        {"name": artist_name}, {"$push": {"uploaded_songs": song_name}}
    )


def delete_song_artist(artist_name: str, song_name: str):
    """Updates the uploaded songs of the artist deleting "song_name"

    Parameters
    ----------
        artist_name (str): Artists's name
        song_name (str) : Song that is going to be deleted of the uploaded songs of the artist


    Raises
    -------
        400 : Bad Request
        404 : Artist Not Found / Song not found

    Returns
    -------
    """

    if not checkValidParameterString(artist_name) or not checkValidParameterString(
        song_name
    ):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    if check_artists_exists(artist_name=artist_name):
        artist_collection.update_one(
            {"name": artist_name}, {"$pull": {"uploaded_songs": song_name}}
        )


def get_artist(name: str) -> Artist:
    """Returns artist with name "name"

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

    artist_data = artist_collection.find_one({"name": name})

    if artist_data is None:
        raise HTTPException(
            status_code=404, detail="El artista con ese nombre no existe"
        )

    date = artist_data["register_date"][:-1]

    return Artist(
        name=artist_data["name"],
        photo=artist_data["photo"],
        register_date=date,
        password=artist_data["password"],
        playback_history=artist_data["playback_history"],
        playlists=artist_data["playlists"],
        saved_playlists=artist_data["saved_playlists"],
        uploaded_songs=artist_data["uploaded_songs"],
    )


def create_artist(name: str, photo: str, password: str):
    """Creates an artist

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
    date_iso8601 = current_date.strftime("%Y-%m-%dT%H:%M:%S")

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    if check_user_exists(name):
        raise HTTPException(
            status_code=400, detail="El nombre de artista ya existe como usuario"
        )

    if check_artists_exists(name):
        raise HTTPException(status_code=400, detail="El artista ya existe")

    hashed_password = security_service.hash_password(password)

    result = artist_collection.insert_one(
        {
            "name": name,
            "photo": photo if "http" in photo else "",
            "register_date": date_iso8601,
            "password": hashed_password,
            "saved_playlists": [],
            "playlists": [],
            "playback_history": [],
            "uploaded_songs": [],
        }
    )

    if not result.acknowledged:
        raise HTTPException(
            status_code=500, detail="Hubo un error durante la creación del artista"
        )


def update_artist(
    name: str,
    photo: str,
    playlists: list,
    saved_playlists: list,
    playback_history: list,
    uploaded_songs: list,
    token: TokenData,
) -> None:
    """Updates a artist , duplicated playlists and songs wont be added

    Parameters
    ----------
        name (str): Artists's name
        photo (str): Url of artist thumbnail
        playlists (list) : artists playlists
        playlists (list) : others artists playlists saved by artist with name "name"
        playback_history (list) : song names of playback history of the artist
        token (TokenData) : token with data of the artist


    Raises
    -------
        400 : Bad Request
        404 : Artist Not Found

    Returns
    -------
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    check_jwt_artist_is_artist(token=token, artist=name)

    result_artist_exists = artist_collection.find_one({"name": name})

    if not result_artist_exists:
        raise HTTPException(status_code=404, detail="El artista no existe")

    artist_collection.update_one(
        {"name": name},
        {
            "$set": {
                "photo": photo if "http" in photo else "",
                "saved_playlists": list(set(saved_playlists)),
                "playlists": list(set(playlists)),
                "playback_history": list(set(playback_history)),
                "uploaded_songs": list(set(uploaded_songs)),
            }
        },
    )


def delete_artist(name: str) -> None:
    """Deletes a artist by name

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

    result = artist_collection.delete_one({"name": name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="El artista no existe")


def get_all_artists() -> list:
    """Returns all artists

    Parameters
    ----------

    Raises
    -------
        400 : Bad Request
        404 : Artist Not Found

    Returns
    -------
        List<Artist>
    """

    artists: list = []
    artists_files = artist_collection.find()

    for artist_file in artists_files:
        artists.append(get_artist(name=artist_file["name"]))

    return artists


def get_play_count_artist(user_name: str) -> int:
    """Returns the total play count of all the artist songs

    Parameters
    ----------
        user_name (str) : Artist name

    Raises
    -------
        400 : Bad Request
        404 : Artist Not Found

    Returns
    -------
        int
    """

    if not checkValidParameterString(user_name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    if not check_artists_exists(user_name):
        raise HTTPException(status_code=404, detail="El artista no existe")

    return song_service.get_artist_playback_count(user_name)


def get_artists(names: list) -> list:
    """Returns a list of Artists that match "names" list of names

    Parameters
    ----------
        names (list): List of artist Names

    Raises
    -------
            400 : Bad Request
            404 : Artist not found

    Returns
    -------
        List<Artist>

    """

    artists: list = []

    for artist_name in names:
        artists.append(get_artist(artist_name))

    return artists


def search_by_name(name: str) -> list[Artist]:
    """Retrieve the artists than match the name

    Args:
        name (str): the name to match

    Returns:
        List[Artist]: a list with the artists that match the name
    """

    artists_names_response = artist_collection.find(
        {"name": {"$regex": name, "$options": "i"}}, {"_id": 0, "name": 1}
    )

    artists_names = []

    [artists_names.append(artist["name"]) for artist in artists_names_response]

    return get_artists(artists_names)


# * AUX METHODs


def add_playback_history(
    user_name: str, song: str, MAX_NUMBER_PLAYBACK_HISTORY_SONGS: int
):
    artist_data = artist_collection.find_one({"name": user_name})

    playback_history = artist_data["playback_history"]

    if len(playback_history) == MAX_NUMBER_PLAYBACK_HISTORY_SONGS:
        playback_history.pop(0)

    playback_history.append(song)

    artist_collection.update_one(
        {"name": user_name}, {"$set": {"playback_history": playback_history}}
    )


def add_saved_playlist(user_name: str, playlist_name: str):
    artist_data = artist_collection.find_one({"name": user_name})

    saved_playlists = artist_data["saved_playlists"]

    saved_playlists.append(playlist_name)

    artist_collection.update_one(
        {"name": user_name}, {"$set": {"saved_playlists": list(set(saved_playlists))}}
    )


def delete_saved_playlist(user_name: str, playlist_name: str):
    artist_data = artist_collection.find_one({"name": user_name})

    saved_playlists = artist_data["saved_playlists"]

    if playlist_name in saved_playlists:
        saved_playlists.remove(playlist_name)

        artist_collection.update_one(
            {"name": user_name}, {"$set": {"saved_playlists": saved_playlists}}
        )


def add_playlist_to_owner(user_name: str, playlist_name: str) -> None:
    artist_data = artist_collection.find_one({"name": user_name})

    playlists = artist_data["playlists"]

    playlists.append(playlist_name)

    artist_collection.update_one(
        {"name": user_name}, {"$set": {"playlists": list(set(playlists))}}
    )


def delete_playlist_from_owner(user_name: str, playlist_name: str) -> None:
    artist_data = artist_collection.find_one({"name": user_name})

    playlists = artist_data["playlists"]

    if playlist_name in playlists:
        playlists.remove(playlist_name)

        artist_collection.update_one(
            {"name": user_name}, {"$set": {"playlists": playlists}}
        )


def update_playlist_name(old_playlist_name: str, new_playlist_name: str) -> None:
    artist_collection.update_many(
        {"saved_playlists": old_playlist_name},
        {"$set": {"saved_playlists.$": new_playlist_name}},
    )
    artist_collection.update_many(
        {"playlists": old_playlist_name},
        {"$set": {"playlists.$": new_playlist_name}},
    )
