"""
Song repository for managing persisted data. These are stored using GridFS, \
    a MongoDB fylesystem for storing BLOB files and its metadata.\
    See https://www.mongodb.com/docs/manual/core/gridfs/

Song files are stored as BLOBs in a separated collection from the metadata
When the song file is not needed, and only the metadata is required use base song services
"""

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
    GetEncodedBytesFromGridFSException,
    SongDAO,
    get_song_dao_from_document,
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
        GetEncodedBytesFromGridFSException: unexpected error getting encoded song file
        SongRepositoryException: unexpected error getting song

    Returns:
        SongDAO: the song
    """
    try:
        metadata_collection = song_collection_provider.get_song_collection()
        file_collection = song_collection_provider.get_gridfs_song_collection()
        song_metadata = metadata_collection.find_one({"name": name})
        song_data = file_collection.find_one({"name": name})
        validate_song_exists(song_metadata)
        song_dao = get_song_dao_from_document(song_metadata, song_data)  # type: ignore

    except SongNotFoundException as exception:
        raise SongNotFoundException from exception
    except GetEncodedBytesFromGridFSException as exception:
        song_repository_logger.exception(f"Error getting encoded song file of song {name}")
        raise SongRepositoryException from exception
    except Exception as exception:
        song_repository_logger.exception(f"Error getting Song {name} from database")
        raise SongRepositoryException from exception
    else:
        song_repository_logger.info(f"Get Song by name returned {song_dao}")
        return song_dao


def create_song(  # noqa: PLR0913
    name: str, artist: str, duration: int, genre: Genre, photo: str, file: bytes
) -> None:
    """Create song

    Args:
        name (str): song name
        artist (str): song artist
        duration (int): song duration in seconds
        genre (Genre): song genre
        photo (str): song photo

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
        song_repository_logger.info(f"Song added to repository : {song}")
