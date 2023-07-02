from services.utils import checkValidParameterString
from database.Database import Database
from gridfs import GridFS
from fastapi import HTTPException
from fastapi.responses import Response
from model.Genre import Genre
from model.Song import Song
import base64
import json


""" Insert songs with format [files,chunks] https://www.mongodb.com/docs/manual/core/gridfs/"""
gridFsSong = GridFS(Database().connection, collection='cancion')
fileSongCollection = Database().connection["cancion.files"]


def get_song(nombre: str) -> Song:
    """ Returns a Song file with attributes and a song encoded in base64 "

    Args:
        nombre (str): Song's name

    Returns:
        Song object

    """

    if nombre is None or nombre == "":
        raise HTTPException(
            status_code=400, detail="El nombre de la canción es vacío")

    song_bytes = gridFsSong.find_one({'name': nombre})
    if song_bytes is None:
        raise HTTPException(
            status_code=404, detail="La canción con ese nombre no existe")

    song_bytes = song_bytes.read()
    # b'ZGF0YSB0byBiZSBlbmNvZGVk'
    encoded_bytes = str(base64.b64encode(song_bytes))

    song_metadata = fileSongCollection.find_one({'name': nombre})

    song = Song(nombre, song_metadata["artist"], song_metadata["photo"], Genre(
        song_metadata["genre"]).name, encoded_bytes)

    return song


def get_songs(nombres: list) -> list:

    songs: list = []

    for song_name in nombres:

        songs.append(get_song(song_name))

    return songs

def get_all_songs() -> list:

    songs: list = []

    songsFiles = fileSongCollection.find()

    for songFile in songsFiles:

        songs.append(get_song(songFile["name"]))

    return songs


def create_song(nombre: str, artista: str, genero: Genre, foto: str, file) -> None:

    if not checkValidParameterString(nombre) or not checkValidParameterString(foto) or not checkValidParameterString(nombre) or not checkValidParameterString(nombre) or not Genre.checkValidGenre(genero.value):
        raise HTTPException(
            status_code=400, detail="Parámetros no válidos o vacíos")

    if fileSongCollection.find_one({'name': nombre}):
        raise HTTPException(status_code=400, detail="La canción ya existe")

    file_id = gridFsSong.put(
        file, name=nombre, artist=artista, genre=str(genero.value), photo=foto)


def get_genres() -> json:

    # Obtener todas las propiedades de la clase Genre
    genre_properties = [(g.name, g.value) for g in Genre]

    genre_dict = dict(genre_properties)
    genre_json = json.dumps(genre_dict)

    return genre_json
