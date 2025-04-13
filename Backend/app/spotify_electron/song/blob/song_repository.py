"""
Song repository for managing persisted data. These are stored using GridFS, \
    a MongoDB fylesystem for storing BLOB files and its metadata.\
    See https://www.mongodb.com/docs/manual/core/gridfs/

Song files are stored as BLOBs in a separated collection from the metadata
When the song file is not needed, and only the metadata is required use base song services
"""

from motor.motor_asyncio import AsyncIOMotorGridOut

import app.spotify_electron.song.blob.providers.song_collection_provider as provider
from app.logging.logging_constants import LOGGING_SONG_BLOB_REPOSITORY
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.genre.genre_schema import Genre
from app.spotify_electron.song.base_song_schema import (
    SongCreateError,
    SongNotFoundError,
    SongRepositoryError,
)
from app.spotify_electron.song.blob.song_schema import (
    SongDAO,
    SongDataNotFoundError,
    SongMetadataDocument,
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

song_repository_logger = SpotifyElectronLogger(LOGGING_SONG_BLOB_REPOSITORY).get_logger()


async def get_song(name: str) -> SongDAO:
    """Get song from database

    Args:
        name (str): song name

    Raises:
        SongNotFoundError: song not found
        SongRepositoryError: unexpected error getting song

    Returns:
        SongDAO: the song
    """
    try:
        metadata_collection = provider.get_blob_song_collection()
        song_metadata = await metadata_collection.find_one({"filename": name})

        validate_song_exists(song_metadata)

        assert song_metadata

        song_dao = get_song_dao_from_document(
            song_name=name,
            document=song_metadata["metadata"],
        )

    except SongNotFoundError as exception:
        song_repository_logger.exception(f"Song not found: {name}")
        raise SongNotFoundError from exception
    except Exception as exception:
        song_repository_logger.exception(f"Error getting Song {name} from database")
        raise SongRepositoryError from exception
    else:
        song_repository_logger.info(f"Get Song by name returned {song_dao}")
        return song_dao


async def create_song(  # noqa: PLR0917
    name: str, artist: str, seconds_duration: int, genre: Genre, photo: str, file: bytes
) -> None:
    """Creates song

    Args:
        name (str): song name
        artist (str): artist name
        seconds_duration (int): song duration on seconds
        genre (Genre): song genre
        photo (str): song photo
        file (bytes): song data

    Raises:
        SongRepositoryError: unexpected error creating song
    """
    try:
        gridfs_collection = provider.get_gridfs_song_collection()

        song = SongMetadataDocument(
            artist=artist,
            seconds_duration=seconds_duration,
            genre=str(genre.value),
            photo=photo,
            streams=0,
            url=f"/stream/{name}",
        )
        result = await gridfs_collection.upload_from_stream(
            filename=name, source=file, metadata=song
        )
        validate_song_create(str(result))
    except SongCreateError as exception:
        song_repository_logger.exception(f"Error inserting Song {name} in database")
        raise SongRepositoryError from exception
    except SongRepositoryError as exception:
        song_repository_logger.exception(f"Unexpected error inserting song {song} in database")
        raise SongRepositoryError from exception
    else:
        song_repository_logger.info(f"Song added to repository: {song}")


async def get_song_data(name: str) -> AsyncIOMotorGridOut:
    """Get song data

    Args:
        name (str): song name

    Raises:
        SongDataNotFoundError: song data doesn't exists
        SongRepositoryError: unexpected error getting song data

    Returns:
        AsyncIOMotorGridOut: song data
    """
    try:
        file_collection = provider.get_gridfs_song_collection()
        song_data = await file_collection.open_download_stream_by_name(name)

        validate_song_data_exists(song_data)

    except SongDataNotFoundError as exception:
        song_repository_logger.exception(f"Song data not found: {name}")
        raise SongDataNotFoundError from exception
    except Exception as exception:
        song_repository_logger.exception(f"Error getting Song {name} from database")
        raise SongRepositoryError from exception
    else:
        song_repository_logger.info("Song data obtained")
        return song_data
