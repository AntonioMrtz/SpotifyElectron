from fastapi import HTTPException

import app.spotify_electron.song.dto_service as dto_service
import app.spotify_electron.user.artist.artist_service as artist_service
import app.spotify_electron.user.base_user_service as base_user_service
from app.database.Database import Database, DatabaseCollection
from app.model.DTO.SongDTO import SongDTO
from app.model.Song import Song
from app.model.SongBlob import SongBlob
from app.spotify_electron.genre.genre_schema import Genre
from app.spotify_electron.security.security_schema import TokenData
from app.spotify_electron.utils.audio_management.audio_management_utils import (
    encode_file,
    get_song_duration_seconds,
)
from app.spotify_electron.utils.validation.validation_utils import validate_parameter

""" Insert songs with format [files,chunks] https://www.mongodb.com/docs/manual/core/gridfs/"""

file_song_collection = Database().get_collection_connection(
    DatabaseCollection.SONG_BLOB_FILE
)
gridFsSong = Database().get_gridfs_collection_connection(
    DatabaseCollection.SONG_BLOB_DATA
)


def check_song_exists(name: str) -> bool:
    """Check if the song exists or not

    Parameters
    ----------
        name (str): Song's name

    Raises
    ------

    Returns
    -------
        Boolean

    """
    return bool(file_song_collection.find_one({"name": name}))


def check_jwt_user_is_song_artist(token: TokenData, artist: str) -> bool:
    """Check if the user is the song artist

    Parameters
    ----------
        token (TokenData): token with the user data
        artist (str) : artist name

    Raises
    ------
        Unauthorized 401

    Returns
    -------
        Boolean

    """
    if token.username == artist:
        return True

    raise HTTPException(
        status_code=401, detail="El usuario no es el creador de la canción"
    )


def get_song(name: str) -> SongBlob:
    """Returns a Song file with attributes and a song encoded in base64 "

    Parameters
    ----------
        name (str): Song's name

    Raises
    ------
        400 : Bad Request
        404 : Song not found

    Returns
    -------
        Song object

    """
    if name is None or name == "":
        raise HTTPException(status_code=400, detail="El nombre de la canción es vacío")

    song_bytes = gridFsSong.find_one({"name": name})
    if song_bytes is None or not check_song_exists(name=name):
        raise HTTPException(
            status_code=404, detail="La canción con ese nombre no existe"
        )

    song_bytes = song_bytes.read()
    # TODO handle exception
    encoded_bytes = encode_file(name, song_bytes)

    song_metadata = file_song_collection.find_one({"name": name})

    return SongBlob(
        name,
        song_metadata["artist"],
        song_metadata["photo"],
        song_metadata["duration"],
        Genre(song_metadata["genre"]).name,
        encoded_bytes,
        song_metadata["number_of_playbacks"],
    )


def get_songs(names: list) -> list:
    """Returns a list of Songs that match "names" list of names  "

    Parameters
    ----------
        names (list): List of song Names

    Raises
    ------
            400 : Bad Request
            404 : Song not found

    Returns
    -------
        List<Song>

    """
    songs: list = []

    for song_name in names:
        songs.append(dto_service.get_song(song_name))

    return songs


def get_all_songs() -> list:
    """Returns a list of all Songs file"

    Parameters
    ----------

    Raises
    ------

    Returns
    -------
        List <Song>

    """
    songs: list = []

    songsFiles = file_song_collection.find()

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
    ------
        400 : Bad Request
        401 : Invalid credentials
        404 : Artist Not Found / Song not found

    Returns
    -------

    """
    artist = token.username

    # TODO check valid genre GenreNotValidException

    if (
        not validate_parameter(name)
        or not validate_parameter(photo)
        or not validate_parameter(artist)
        or not Genre.check_valid_genre(genre.value)
    ):
        raise HTTPException(status_code=400, detail="Parámetros no válidos o vacíos")

    base_user_service.validate_user_should_exists(artist)

    if check_song_exists(name=name):
        raise HTTPException(status_code=400, detail="La canción ya existe")

    song_duration = get_song_duration_seconds(name, file)

    gridFsSong.put(
        file,
        name=name,
        artist=artist,
        duration=song_duration,
        genre=str(genre.value),
        photo=photo,
        number_of_playbacks=0,
    )

    artist_service.add_song_artist(artist, name)


def delete_song(name: str) -> None:
    """Delete the song with his asociated chunk files "

    Parameters
    ----------
        name (str): Song's name

    Raises
    ------
        400 : Bad Parameters
        404 : Artist not found

    Returns
    -------

    """
    if not validate_parameter(name):
        raise HTTPException(
            status_code=400, detail="El nombre de la canción no es válido"
        )

    result = file_song_collection.find_one({"name": name})

    if result and result["_id"]:
        artist_service.delete_song_from_artist(result["artist"], name)
        gridFsSong.delete(result["_id"])

    else:
        raise HTTPException(status_code=404, detail="La canción no existe")


def update_song(
    name: str, nuevo_nombre: str, photo: str, genre: Genre, token: TokenData
) -> None:
    """Updates a song with name, url of thumbnail, duration, genre and number of plays, if empty parameter is not being updated "

    Parameters
    ----------
        name (str): Song's name
        nuevo_nombre (str) : New Song's name, if empty name is not being updated
        photo (str): Url of Song thumbnail
        genre (Genre): Genre of the Song
        number_of_playbacks (int): Number of plays of the Song
        token (TokenData) : token data of the user

    Raises
    ------
        400 : Bad Request
        401 : Unauthorized
        404 : Song Not Found

    Returns
    -------

    """
    if not validate_parameter(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result_song_exists = get_song(name=name)

    if not result_song_exists:
        raise HTTPException(status_code=404, detail="La cancion no existe")

    check_jwt_user_is_song_artist(token, result_song_exists.artist)

    if validate_parameter(nuevo_nombre):
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
                        if genre is not None
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
                        if genre is not None
                        else Genre[result_song_exists.genre].value
                    ),
                }
            },
        )


def increase_number_playbacks(name: str) -> None:
    """Increase the number of plays of a song

    Parameters
    ----------
        name (str): Song's name

    Raises
    ------
        400 : Bad Request
        404 : Song Not Found

    Returns
    -------

    """
    if not validate_parameter(name):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    result_song_exists = get_song(name=name)

    if not result_song_exists:
        raise HTTPException(status_code=404, detail="La cancion no existe")

    file_song_collection.update_one(
        {"name": name},
        {"$set": {"number_of_playbacks": result_song_exists.number_of_playbacks + 1}},
    )


def search_by_name(name: str) -> list[SongDTO]:
    """Retrieve the songs than match the name

    Args:
    ----
        name (str): the name to match

    Returns:
    -------
        List[SongDTO]: a list with the songs that match the name

    """
    song_names_response = file_song_collection.find(
        {"name": {"$regex": name, "$options": "i"}}, {"_id": 0, "name": 1}
    )

    song_names = []

    [song_names.append(song["name"]) for song in song_names_response]

    return dto_service.get_songs(song_names)


def get_artist_playback_count(artist_name: str) -> int:
    """The total playback count for all artist songs

    Args:
    ----
        artist_name (str): the artist name

    Returns:
    -------
        int: the number of playback count for the artists songs

    """
    result_number_playback_count_query = file_song_collection.aggregate(
        [
            {"$match": {"artist": artist_name}},
            {"$group": {"_id": None, "total": {"$sum": "$number_of_playbacks"}}},
        ]
    )
    result_number_playback_count_query = next(result_number_playback_count_query, None)

    if result_number_playback_count_query is None:
        return 0
    return result_number_playback_count_query["total"]


def get_songs_metadata_by_genre(genre: Genre) -> list[Song]:
    # TODO
    # TODO hanlde GenreNotValidException
    result_get_song_by_genre = file_song_collection.find(
        {"genre": Genre.get_genre_string_value(genre)}
    )
    songs_by_genre = []

    for song_data in result_get_song_by_genre:
        songs_by_genre.append(
            Song(
                name=song_data["name"],
                artist=song_data["artist"],
                photo=song_data["photo"],
                seconds_duration=song_data["duration"],
                genre=Genre(song_data["genre"]).name,
                number_of_playbacks=song_data["number_of_playbacks"],
                url="no_url_get_songs_by_genre",
            )
        )

    return songs_by_genre
