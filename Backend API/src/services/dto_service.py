from model.DTO.SongDTO import SongDTO
from model.DTO.PlaylistDTO import PlaylistDTO
from database.Database import Database
from model.Genre import Genre
from fastapi import HTTPException
from services.utils import checkValidParameterString
from sys import modules

if "pytest" in modules:

    song_collection = Database().connection["test.canciones.streaming"]
    playlistCollection = Database().connection["test.playlist"]

else:

    song_collection = Database().connection["canciones.streaming"]
    playlistCollection = Database().connection["playlist"]


def get_song(name: str) -> SongDTO:
    """ Returns a song's metadata without his audio file"

    Parameters
    ----------
        name (str) : name of the song

    Raises
    -------
        400 : Bad Request
        404 : Song not found

    Returns
    -------
        SongDTO
    """
    if not checkValidParameterString(name):
        raise HTTPException(
            status_code=400, detail="El nombre de la canción es vacío")

    song_data = song_collection.find_one({'name': name})
    if song_data is None:
        raise HTTPException(
            status_code=404, detail="La canción con ese nombre no existe")

    return SongDTO(name=song_data["name"], artist=song_data["artist"], photo=song_data["photo"], duration=song_data["duration"], genre=Genre(song_data["genre"]).name, number_of_plays=song_data["number_of_plays"])


def get_songs(song_names: list) -> list:
    """ Returns a list with song's metadatas without his audio files"

    Parameters
    ----------
        song_names (list) : song names

    Raises
    -------
        400 : Bad Request
        404 : Song not found

    Returns
    -------
        List<SongDTO>
    """

    respone_songs_dto = []

    for name in song_names:

        if not checkValidParameterString(name):
            raise HTTPException(
                status_code=400, detail="El nombre de la canción es vacío")

        song_data = song_collection.find_one({'name': name})
        if song_data is None:
            raise HTTPException(
                status_code=404, detail="La canción con ese nombre no existe")

        respone_songs_dto.append(SongDTO(name=song_data["name"], artist=song_data["artist"], photo=song_data["photo"], duration=song_data["duration"], genre=Genre(
            song_data["genre"]).name, number_of_plays=song_data["number_of_plays"]))

    return respone_songs_dto


def get_playlist(name: str) -> PlaylistDTO:
    """ Returns a playlist's metadata without his song's audio files"

    Parameters
    ----------
        name (str) : name of the playlist

    Raises
    -------
        400 : Bad Request
        404 : Playlist not found

    Returns
    -------
        PlaylistDTO
    """

    if not checkValidParameterString(name):
        raise HTTPException(
            status_code=400, detail="El nombre de la playlist es vacío")

    playlist_data = playlistCollection.find_one({'name': name})

    if playlist_data is None:
        raise HTTPException(
            status_code=404, detail="La playlist con ese nombre no existe")

    return PlaylistDTO(name=playlist_data["name"], photo=playlist_data["photo"], description=playlist_data["description"], upload_date=playlist_data["upload_date"], song_names=playlist_data["song_names"], owner=playlist_data["owner"])


def get_songs_by_genero(genre: Genre) -> list:
    """ Increase the number of plays of a song

    Parameters
    ----------
        name (str): Song's name

    Raises
    -------
        400 : Bad Request
        404 : Song Not Found

    Returns
    -------
    List<Song>

    """

    if not checkValidParameterString(genre.value):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    if not Genre.checkValidGenre(genre.value):
        raise HTTPException(status_code=404, detail="El género no existe")

    result_get_song_by_genre = song_collection.find(
        {'genre': Genre.getGenre(genre)})

    songs_by_genre = []

    for song_data in result_get_song_by_genre:

        songs_by_genre.append(SongDTO(name=song_data["name"], artist=song_data["artist"], photo=song_data["photo"], duration=song_data["duration"], genre=Genre(
            song_data["genre"]).name, number_of_plays=song_data["number_of_plays"]))

    return songs_by_genre
