from services.utils import checkValidParameterString
from database.Database import Database
from gridfs import GridFS
from fastapi import HTTPException
from fastapi.responses import Response
from model.Genre import Genre
from model.Song import Song
from pydub import AudioSegment
from lameenc import Encoder
import base64
import json
import io
import mutagen
from mutagen.wave import WAVE
from mutagen.mp3 import MP3
import wave
import ffmpeg
import librosa




""" Insert songs with format [files,chunks] https://www.mongodb.com/docs/manual/core/gridfs/"""
gridFsSong = GridFS(Database().connection, collection='cancion')
fileSongCollection = Database().connection["cancion.files"]


def get_song(name: str) -> Song:
    """ Returns a Song file with attributes and a song encoded in base64 "

    Args:
        name (str): Song's name

    Raises:
        400 : Bad Request
        404 : Song not found

    Returns:
        Song object
    """

    if name is None or name == "":
        raise HTTPException(
            status_code=400, detail="El nombre de la canción es vacío")

    song_bytes = gridFsSong.find_one({'name': name})
    if song_bytes is None:
        raise HTTPException(
            status_code=404, detail="La canción con ese nombre no existe")

    song_bytes = song_bytes.read()
    # b'ZGF0YSB0byBiZSBlbmNvZGVk'
    encoded_bytes = str(base64.b64encode(song_bytes))

    song_metadata = fileSongCollection.find_one({'name': name})

    song = Song(name, song_metadata["artist"], song_metadata["photo"], song_metadata["duration"], Genre(
        song_metadata["genre"]).name, encoded_bytes)

    return song


def get_songs(names: list) -> list:
    """ Returns a list of Songs that match "names" list of names  "

    Args:
        names (list): List of song Names

    Raises:
            400 : Bad Request
            404 : Song not found

    Returns:
        List<Song>

    """

    songs: list = []

    for song_name in names:

        songs.append(get_song(song_name))

    return songs


def get_all_songs() -> list:
    """ Returns a list of all Songs file"

    Args:

    Returns:
        List <Song>

    """

    songs: list = []

    songsFiles = fileSongCollection.find()

    for songFile in songsFiles:

        songs.append(get_song(songFile["name"]))

    return songs


def convert_to_mp3(input_data, bitrate=128):
    # Load the audio from the binary input_data
    audio = AudioSegment.from_file(io.BytesIO(input_data))

    # If the audio is not already in MP3 format, convert it
    if audio.format != "mp3":
        # Encode the audio as MP3 using lameenc
        encoder = Encoder()
        encoder.set_bit_rate(bitrate)
        encoder.set_in_sample_rate(audio.frame_rate)
        encoder.set_channels(audio.channels)
        encoder.set_quality(2)  # 2 = high quality, 7 = low quality
        audio_data = encoder.encode(audio.raw_data)
        encoder.close()

        return audio_data

    return input_data


async def create_song(name: str, artist: str, genre: Genre, photo: str, file) -> None:
    """ Returns a Song file with attributes and a song encoded in base64 "

    Args:
        name (str): Song's name
        artist (str) : Artist name
        genre : Genre of the song
        photo (str) : Url of the song thumbnail
        file : Mp3 file of the song

    Raises:
        400 : Bad Request

    Returns:
    """

    if not checkValidParameterString(name) or not checkValidParameterString(photo) or not checkValidParameterString(artist) or not Genre.checkValidGenre(genre.value):
        raise HTTPException(
            status_code=400, detail="Parámetros no válidos o vacíos")

    if fileSongCollection.find_one({'name': name}):
        raise HTTPException(status_code=400, detail="La canción ya existe")

    binary_data_bytes = base64.b64decode(file)

    #s = io.BytesIO(binary_data_bytes)

    s = io.BytesIO(binary_data_bytes)

    # Assuming 'audio_bytes' contains the audio data in bytes
    audio_data, sample_rate = librosa.load(io.BytesIO(file), sr=None)

    # Calculate the duration in seconds
    duration = librosa.get_duration(y=audio_data, sr=sample_rate)
    print(duration)





    """ file_id = gridFsSong.put(
        file, name=name, artist=artist,duration=duration ,genre=str(genre.value), photo=photo) """


def get_genres() -> json:
    """ Returns a json with all the available genres"

    Args:

    Returns:
        Json { GenreEnum : 'genre'}
    """

    # Obtener todas las propiedades de la clase Genre
    genre_properties = [(g.name, g.value) for g in Genre]

    genre_dict = dict(genre_properties)
    genre_json = json.dumps(genre_dict)

    return genre_json
