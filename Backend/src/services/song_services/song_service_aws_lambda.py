import base64
import io
from sys import modules
from typing import List

import librosa
import requests
import src.services.artist_service as artist_service
from fastapi import HTTPException
from pymongo.errors import PyMongoError
from src.boostrap.PropertiesManager import PropertiesManager
from src.constants.set_up_constants import LAMBDA_URL_ENV_NAME
from src.database.Database import Database
from src.model.Genre import Genre
from src.model.Song import Song
from src.model.TokenData import TokenData
from src.services.utils import checkValidParameterString

""" Insert songs with format [files,chunks] https://www.mongodb.com/docs/manual/core/gridfs/"""

if "pytest" in modules:
    file_song_collection = Database().connection["test.cancion.files"]
    song_collection = Database().connection["test.canciones.streaming"]


else:
    file_song_collection = Database().connection["cancion.files"]
    song_collection = Database().connection["canciones.streaming"]


def check_song_exists(name: str) -> bool:
    """Check if the song exists or not

    Parameters
    ----------
        name (str): Song's name

    Raises
    -------

    Returns
    -------
        Boolean
    """

    return True if song_collection.find_one({"name": name}) else False


def check_jwt_user_is_song_artist(token: TokenData, artist: str) -> bool:
    """Check if the user is the song artist

    Parameters
    ----------
        token (TokenData): token with the user data
        artist (str) : artist name

    Raises
    -------
        Unauthorized 401

    Returns
    -------
        Boolean
    """

    if token.username == artist:
        return True
    else:
        raise HTTPException(
            status_code=401, detail="El usuario no es el creador de la canción"
        )


def get_song(name: str) -> Song:
    """Returns a Song file with attributes and streaming url "

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
        raise HTTPException(status_code=400, detail="El nombre de la canción es vacío")

    song = song_collection.find_one({"name": name})
    if song is None or not check_song_exists(name=name):
        raise HTTPException(
            status_code=404, detail="La canción con ese nombre no existe"
        )

    try:
        params = {
            "nombre": name,
        }
        res = requests.get(
            f"{getattr(PropertiesManager,LAMBDA_URL_ENV_NAME)}", params=params
        )
        if res.status_code != 200:
            # TODO
            raise ClientError(
                {"Error": {"Code": res.status_code, "Message": res.content}},
                "operation_name",
            )

        response_json = res.json()
        cloudfront_url = response_json["url"]

        song = Song(
            name=name,
            artist=song["artist"],
            photo=song["photo"],
            duration=song["duration"],
            genre=Genre(song["genre"]).name,
            url=cloudfront_url,
            number_of_plays=song["number_of_plays"],
        )

        return song
    except ClientError as e:
        # TODO
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor al interactuar con AWS {e}",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo subir la canción {e}")


def get_songs(names: list) -> list:
    """Returns a list of Songs that match "names" list of names  "

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
    """Returns a list of all Songs file"

    Parameters
    ----------

    Raises
    -------

    Returns
    -------
        List <Song>

    """

    songs: list = []

    songsFiles = song_collection.find()

    for songFile in songsFiles:
        songs.append(get_song(songFile["name"]))

    return songs


async def create_song(
    name: str, genre: Genre, photo: str, file, token: TokenData
) -> None:
    """Returns a Song file with attributes and a song encoded in base64 "

    Parameters
    ----------
        name (str): Song's name
        genre (Genre): Genre of the song
        photo (str) : Url of the song thumbnail
        file (FileUpload): Mp3 file of the song
        token (TokenData) : jwt token decoded


    Raises
    -------
        400 : Bad Request
        401 : Invalid credentials
        404 : Artist Not Found / Song not found

    Returns
    -------
    """
    artist = token.username

    if (
        not checkValidParameterString(name)
        or not checkValidParameterString(photo)
        or not checkValidParameterString(artist)
        or not Genre.checkValidGenre(genre.value)
    ):
        raise HTTPException(status_code=400, detail="Parámetros no válidos o vacíos")

    if check_song_exists(name=name):
        raise HTTPException(status_code=400, detail="La canción ya existe")

    if not artist_service.check_artists_exists(artist_name=artist):
        raise HTTPException(status_code=404, detail="El artista no existe")

    try:
        # Assuming 'audio_bytes' contains the audio data in bytes
        audio_data, sample_rate = librosa.load(io.BytesIO(file), sr=None)

        # Calculate the duration in seconds
        duration = librosa.get_duration(y=audio_data, sr=sample_rate)

    #! If its not a sound file
    except:
        duration = 0

    try:
        # b'ZGF0YSB0byBiZSBlbmNvZGVk'
        encoded_bytes = str(base64.b64encode(file))

        params = {"nombre": name}

        request_data_body = {
            "file": encoded_bytes,
        }
        res = requests.post(
            f"{getattr(PropertiesManager,LAMBDA_URL_ENV_NAME)}",
            json=request_data_body,
            params=params,
        )
        if res.status_code != 201:
            # TODO
            raise ClientError(
                {"Error": {"Code": res.status_code, "Message": res.content}},
                "operation_name",
            )

        file_id = song_collection.insert_one(
            {
                "name": name,
                "artist": artist,
                "duration": duration,
                "genre": str(genre.value),
                "photo": photo,
                "number_of_plays": 0,
            }
        )
        artist_service.add_song_artist(artist, name)

    except PyMongoError as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al interactuar con MongoDB",
        )

    except ClientError as e:
        # TODO
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor al interactuar con AWS {e}",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo subir la canción {e}")


def delete_song(name: str) -> None:
    """Delete the song with his asociated chunk files "

    Parameters
    ----------
        name (str): Song's name

    Raises
    -------
        400 : Bad Parameters
        404 : Artist not found

    Returns
    -------
    """

    if not checkValidParameterString(name):
        raise HTTPException(
            status_code=400, detail="El nombre de la canción no es válido"
        )

    result = song_collection.find_one({"name": name})

    if not result or not result["_id"]:
        raise HTTPException(status_code=404, detail="La canción no existe")

    try:
        params = {
            "nombre": name,
        }
        res = requests.delete(
            f"{getattr(PropertiesManager,LAMBDA_URL_ENV_NAME)}", params=params
        )
        if res.status_code != 202:
            # TODO
            raise ClientError(
                {"Error": {"Code": res.status_code, "Message": res.content}},
                "operation_name",
            )

        song_collection.delete_one({"name": name})
        artist_service.delete_song_artist(result["artist"], name)

    except PyMongoError as e:
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al interactuar con MongoDB",
        )

    except ClientError as e:
        # TODO
        raise HTTPException(
            status_code=500, detail="Error interno del servidor al interactuar con AWS"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail="No se pudo subir la canción")


# ? NOT USED
def update_song(
    name: str, nuevo_nombre: str, photo: str, genre: Genre, token: TokenData
) -> None:
    # TODO, check if correct ( file_song_collection...)
    """Updates a song with name, url of thumbnail, duration, genre and number of plays, if empty parameter is not being updated "

    Parameters
    ----------
        name (str): Song's name
        nuevo_nombre (str) : New Song's name, if empty name is not being updated
        photo (str): Url of Song thumbnail
        genre (Genre): Genre of the Song
        number_of_plays (int): Number of plays of the Song
        token (TokenData) : token data of the user

    Raises
    -------
        400 : Bad Request
        401 : Unauthorized
        404 : Song Not Found

    Returns
    -------
    """

    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result_song_exists: Song = get_song(name=name)

    if not result_song_exists:
        raise HTTPException(status_code=404, detail="La cancion no existe")

    check_jwt_user_is_song_artist(token, result_song_exists.artist)

    if checkValidParameterString(nuevo_nombre):
        new_name = nuevo_nombre
        file_song_collection.update_one(
            {"name": name},
            {
                "$set": {
                    "name": new_name,
                    "artist": result_song_exists.artist,
                    "photo": (
                        photo if photo and "http" in photo else result_song_exists.photo
                    ),
                    "genre": (
                        Genre(genre).value
                        if genre != None
                        else Genre[result_song_exists.genre].value
                    ),
                }
            },
        )
    else:
        file_song_collection.update_one(
            {"name": name},
            {
                "$set": {
                    "name": name,
                    "artist": result_song_exists.artist,
                    "photo": (
                        photo if photo and "http" in photo else result_song_exists.photo
                    ),
                    "genre": (
                        Genre(genre).value
                        if genre != None
                        else Genre[result_song_exists.genre].value
                    ),
                }
            },
        )


def increase_number_plays(name: str) -> None:
    """Increase the number of plays of a song

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

    song_collection.update_one(
        {"name": name},
        {"$set": {"number_of_plays": result_song_exists.number_of_plays + 1}},
    )


def search_by_name(name: str) -> list:
    """Returns a list of Songs that contains "name" in their names

    Parameters
    ----------
        names (list): List of song Names

    Raises
    -------
            400 : Bad Request
            404 : Song not found

    Returns
    -------
        List<Json>
    """

    song_names_response = song_collection.find(
        {"name": {"$regex": name, "$options": "i"}}, {"_id": 0, "name": 1}
    )

    song_names = []

    [song_names.append(song["name"]) for song in song_names_response]

    songs = get_songs(song_names)

    songs_json_list = []

    [songs_json_list.append(song.get_json()) for song in songs]

    return songs_json_list


def get_artist_playback_count(artist_name: str) -> int:
    """The total playback count for all artist songs

    Args:
        artist_name (str): the artist name

    Returns:
        int: the number of playback count for the artists songs
    """
    result_number_playback_count_query = song_collection.aggregate(
        [
            {"$match": {"artist": artist_name}},
            {"$group": {"_id": None, "total": {"$sum": "$number_of_plays"}}},
        ]
    )
    result_number_playback_count_query = next(result_number_playback_count_query, None)

    if result_number_playback_count_query is None:
        return 0
    total_plays = result_number_playback_count_query["total"]
    return total_plays


def get_songs_by_genre(genre: Genre) -> List[Song]:
    # TODO
    result_get_song_by_genre = song_collection.find({"genre": Genre.getGenre(genre)})
    songs_by_genre = []

    for song_data in result_get_song_by_genre:
        songs_by_genre.append(
            Song(
                name=song_data["name"],
                artist=song_data["artist"],
                photo=song_data["photo"],
                duration=song_data["duration"],
                genre=Genre(song_data["genre"]).name,
                number_of_plays=song_data["number_of_plays"],
                url="no_url_get_songs_by_genre",
            )
        )

    return songs_by_genre


# TODO convertir json -> Song objeto
