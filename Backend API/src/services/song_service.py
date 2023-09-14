from services.utils import checkValidParameterString
from database.Database import Database
from gridfs import GridFS
from fastapi import HTTPException
from fastapi.responses import Response
from model.Genre import Genre
from model.Song import Song
import base64
import json
import io
import librosa


""" Insert songs with format [files,chunks] https://www.mongodb.com/docs/manual/core/gridfs/"""
gridFsSong = GridFS(Database().connection, collection='cancion')
fileSongCollection = Database().connection["cancion.files"]



def check_song_exists(name:str) -> bool:
    """ Check if the song exists or not

    Parameters
    ----------
        name (str): Song's name

    Raises
    -------

    Returns
    -------
        Boolean
    """
    return True if fileSongCollection.find_one({'name': name}) else False



def get_song(name: str) -> Song:
    """ Returns a Song file with attributes and a song encoded in base64 "

    Parameters
    ----------
        name (str): Song's name

    Raises
    -------
        400 : Bad Request
        404 : Song not found

    Returns
    -------
        Song object
    """

    if name is None or name == "":
        raise HTTPException(
            status_code=400, detail="El nombre de la canción es vacío")

    song_bytes = gridFsSong.find_one({'name': name})
    if song_bytes is None or not check_song_exists(name=name):
        raise HTTPException(
            status_code=404, detail="La canción con ese nombre no existe")

    song_bytes = song_bytes.read()
    # b'ZGF0YSB0byBiZSBlbmNvZGVk'
    encoded_bytes = str(base64.b64encode(song_bytes))

    song_metadata = fileSongCollection.find_one({'name': name})

    song = Song(name, song_metadata["artist"], song_metadata["photo"], song_metadata["duration"], Genre(
        song_metadata["genre"]).name, encoded_bytes, song_metadata["number_of_plays"])

    return song


def get_songs(names: list) -> list:
    """ Returns a list of Songs that match "names" list of names  "

    Parameters
    ----------
        names (list): List of song Names

    Raises
    -------
            400 : Bad Request
            404 : Song not found

    Returns
    -------
        List<Song>

    """

    songs: list = []

    for song_name in names:

        songs.append(get_song(song_name))

    return songs


def get_all_songs() -> list:
    """ Returns a list of all Songs file"

    Parameters
    ----------

    Raises
    -------

    Returns
    -------
        List <Song>

    """

    songs: list = []

    songsFiles = fileSongCollection.find()

    for songFile in songsFiles:

        songs.append(get_song(songFile["name"]))

    return songs


async def create_song(name: str, artist: str, genre: Genre, photo: str, file) -> None:
    """ Returns a Song file with attributes and a song encoded in base64 "

    Parameters
    ----------
        name (str): Song's name
        artist (str) : Artist name
        genre (Genre): Genre of the song
        photo (str) : Url of the song thumbnail
        file (FileUpload): Mp3 file of the song

    Raises
    -------
        400 : Bad Request

    Returns
    -------
    """

    if not checkValidParameterString(name) or not checkValidParameterString(photo) or not checkValidParameterString(artist) or not Genre.checkValidGenre(genre.value):
        raise HTTPException(
            status_code=400, detail="Parámetros no válidos o vacíos")

    if check_song_exists(name=name):
        raise HTTPException(status_code=400, detail="La canción ya existe")

    try:
        # Assuming 'audio_bytes' contains the audio data in bytes
        audio_data, sample_rate = librosa.load(io.BytesIO(file), sr=None)

        # Calculate the duration in seconds
        duration = librosa.get_duration(y=audio_data, sr=sample_rate)

        file_id = gridFsSong.put(
            file, name=name, artist=artist, duration=duration, genre=str(genre.value), photo=photo, number_of_plays=0)

    #! If its not a sound file
    except:
        duration = 0

        file_id = gridFsSong.put(
            file, name=name, artist=artist, duration=duration, genre=str(genre.value), photo=photo, number_of_plays=0)


def delete_song(name: str) -> None:
    """ Delete the song with his asociated chunk files "

    Parameters
    ----------
        name (str): Song's name

    Raises
    -------
        400 : Bad Parameters
        404 : Bad Request

    Returns
    -------
    """

    if not checkValidParameterString(name):
        raise HTTPException(
            status_code=400, detail="El nombre de la canción no es válido")

    result = fileSongCollection.find_one({'name': name})

    if result and result["_id"]:
        gridFsSong.delete(result["_id"])

    else:
        raise HTTPException(status_code=404, detail="La canción no existe")


def update_song(name: str, nuevo_nombre: str, photo: str, genre: Genre) -> None:
    """ Updates a song with name, url of thumbnail, duration, genre and number of plays, if empty parameter is not being updated "

    Parameters
    ----------
        name (str): Song's name
        nuevo_nombre (str) : New Song's name, if empty name is not being updated
        photo (str): Url of Song thumbnail
        genre (Genre): Genre of the Song
        number_of_plays (int): Number of plays of the Song

    Raises
    -------
        400 : Bad Request
        404 : Song Not Found

    Returns
    -------
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result_song_exists: Song = get_song(name=name)

    if not result_song_exists:
        raise HTTPException(status_code=404, detail="La cancion no existe")

    if checkValidParameterString(nuevo_nombre):
        new_name = nuevo_nombre
        fileSongCollection.update_one({'name': name}, {
            "$set": {'name': new_name, 'artist': result_song_exists.artist, 'photo': photo if photo and 'http' in photo else result_song_exists.photo, 'genre': Genre(genre).value if genre != None else Genre[result_song_exists.genre].value}})
    else:
        fileSongCollection.update_one({'name': name}, {
            "$set": {'name': name, 'artist': result_song_exists.artist, 'photo': photo if photo and 'http' in photo else result_song_exists.photo, 'genre': Genre(genre).value if genre != None else Genre[result_song_exists.genre].value}})


def increase_number_plays(name: str) -> None:
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
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result_song_exists: Song = get_song(name=name)

    if not result_song_exists:
        raise HTTPException(status_code=404, detail="La cancion no existe")

    fileSongCollection.update_one({'name': name}, {
        "$set": {'number_of_plays': result_song_exists.number_of_plays+1}})
