"""
Song repository for managing persisted data. These are stored using GridFS, \
    a MongoDB fylesystem for storing BLOB files and its metadata.\
    See https://www.mongodb.com/docs/manual/core/gridfs/

Song files are stored as BLOBs in a separated collection from the metadata
When the song file is not needed, and only the metadata is required use base song services
"""

from gridfs import GridOut

import app.spotify_electron.song.providers.song_collection_provider as song_collection_provider
from app.logging.logging_constants import LOGGING_SONG_BLOB_REPOSITORY
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.genre.genre_schema import Genre
from app.spotify_electron.song.base_song_schema import (
    SongCreateException,
    SongNotFoundException,
    SongRepositoryException,
)
from app.spotify_electron.song.blob.song_schema import (
    SongDAO,
    SongDataNotFoundException,
    get_song_dao_from_document,
)
from app.spotify_electron.song.blob.validations.song_repository_validations import (
    validate_song_data_exists,
)
from app.spotify_electron.song.blob.validations.song_service_validations import (
    validate_song_create,
)
from app.spotify_electron.song.validations.base_song_repository_validations import (
    validate_song_exists,
)

song_repository_logger = SpotifyElectronLogger(LOGGING_SONG_BLOB_REPOSITORY).getLogger()


def get_song(name: str) -> SongDAO:
    """Get song from database

    Args:
        name (str): song name

    Raises:
        SongNotFoundException: song not found
        SongRepositoryException: unexpected error getting song

    Returns:
        SongDAO: the song
    """
    try:
        metadata_collection = song_collection_provider.get_song_collection()
        song_metadata = metadata_collection.find_one({"name": name})
        validate_song_exists(song_metadata)
        song_dao = get_song_dao_from_document(song_metadata)  # type: ignore

    except SongNotFoundException as exception:
        song_repository_logger.exception(f"Song not found: {name}")
        raise SongNotFoundException from exception
    except Exception as exception:
        song_repository_logger.exception(f"Error getting Song {name} from database")
        raise SongRepositoryException from exception
    else:
        song_repository_logger.info(f"Get Song by name returned {song_dao}")
        return song_dao


def create_song(  # noqa: PLR0917
    name: str, artist: str, duration: int, genre: Genre, photo: str, file: bytes
) -> None:
    """Create song

    Args:
        name (str): song name
        artist (str): song artist
        duration (int): song duration in seconds
        genre (Genre): song genre
        photo (str): song photo
        file (bytes): song content

    Raises:
        SongRepositoryException: unexpected error creating song
    """
    try:
        gridfs_collection = song_collection_provider.get_gridfs_song_collection()
        song = {
            "name": name,
            "artist": artist,
            "duration": duration,
            "genre": str(genre.value),
            "photo": photo,
            "streams": 0,
            "url": f"/stream/{name}",
        }
        result = gridfs_collection.put(
            file,
            **song,
        )
        validate_song_create(result)
    except SongCreateException as exception:
        song_repository_logger.exception(f"Error inserting Song {name} in database")
        raise SongRepositoryException from exception
    except SongRepositoryException as exception:
        song_repository_logger.exception(f"Unexpected error inserting song {song} in database")
        raise SongRepositoryException from exception
    else:
        song_repository_logger.info(f"Song added to repository: {song}")


def get_song_data(name: str) -> GridOut:
    """Get song data

    Args:
        name (str): song name

    Raises:
        SongDataNotFoundException: song data doesn't exists
        SongRepositoryException: unexpected error getting song data

    Returns:
        GridOut: song data
    """
    try:
        file_collection = song_collection_provider.get_gridfs_song_collection()
        song_data = file_collection.find_one({"name": name})
        validate_song_data_exists(song_data)

    except SongDataNotFoundException as exception:
        song_repository_logger.exception(f"Song data not found: {name}")
        raise SongDataNotFoundException from exception
    except Exception as exception:
        song_repository_logger.exception(f"Error getting Song {name} from database")
        raise SongRepositoryException from exception
    else:
        song_repository_logger.info("Song data obtained")
        return song_data  # type: ignore
