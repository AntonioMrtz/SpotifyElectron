from database.Database import Database
import services.song_service as song_service
import services.dto_service as dto_service
from model.Playlist import Playlist
from model.Song import Song
from fastapi import HTTPException
from services.utils import checkValidParameterString

playlistCollection = Database().connection["playlist"]


def get_playlist(name: str) -> Playlist:
    """ Returns a Playlist with his songs"

    Args:
        name (str): Playlists's name

    Raises:
        400 : Bad Request
        404 : Playlist not found

    Returns:
        Playlist object
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    playlist_data = playlistCollection.find_one({'name': name})

    if playlist_data is None:
        raise HTTPException(
            status_code=404, detail="La playlist con ese nombre no existe")

    playlist_songs = []

    [playlist_songs.append(song_service.get_song(song_name))
     for song_name in playlist_data["song_names"]]

    #[print(song.name) for song in playlist_songs]

    playlist = Playlist(name, playlist_data["photo"], playlist_songs)

    return playlist


def create_playlist(name: str, photo: str, song_names: list) -> None:
    """ Create a playlist with name, url of thumbnail and list of song names

    Args:
        name (str): Playlists's name
        photo (str): Url of playlist thumbnail
        song_names (list<str>): List of song names of the playlist

    Raises:
        400 : Bad Request

    Returns:
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    songs = song_service.get_songs(song_names)
    result_playlist_exists = playlistCollection.find_one({'name': name})

    if result_playlist_exists:
        raise HTTPException(status_code=400, detail="La playlist ya existe")

    result = playlistCollection.insert_one(
        {'name': name, 'photo': photo if 'http' in photo else '', 'song_names': song_names})

    return True if result.acknowledged else False


def update_playlist(name: str, photo: str, song_names: list) -> None:
    """ Updates a playlist with name, url of thumbnail and list of song names [ duplicates wont be added ]

    Args:
        name (str): Playlists's name
        photo (str): Url of playlist thumbnail
        song_names (list<str>): List of song names of the playlist

    Raises:
        400 : Bad Request
        404 : Playlist Not Found

    Returns:
    """




    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result_playlist_exists = playlistCollection.find_one({'name': name})

    if not result_playlist_exists:
        raise HTTPException(status_code=404, detail="La playlist no existe")

    playlistCollection.update_one({'name': name}, {
                                  "$set": {'name': name, 'photo': photo, 'song_names': list(set(song_names))}})


def get_all_playlist() -> list:
    """ Returns all playlists in a DTO object"

    Args:

    Raises:

    Returns:
        List<PlaylistDTO>
    """

    playlists: list = []
    playlists_files = playlistCollection.find()

    for playlist_file in playlists_files:
        playlists.append(dto_service.get_playlist(playlist_file["name"]))

    return playlists
