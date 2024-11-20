"""
Common validations for all Song services, regardless of the current architecture
"""

from pymongo.results import DeleteResult, InsertOneResult

from app.spotify_electron.song.base_song_schema import (
    BaseSongDAO,
    SongCreateException,
    SongDeleteException,
    SongNotFoundException,
)


def validate_song_exists(song: BaseSongDAO | None) -> None:
    """Validates that a song exists.

    Args:
       song: The song to validate.

    Raises:
       SongNotFoundException: If the song is None.
    """
    if song is None:
        raise SongNotFoundException


def validate_base_song_create(result: InsertOneResult) -> None:
    """Validates that a song was successfully created.

    Args:
       result: Result from the database insertion operation.

    Raises:
       SongCreateException: If the song insertion was not acknowledged.
    """
    if not result.acknowledged:
        raise SongCreateException


def validate_song_delete_count(result: DeleteResult) -> None:
    """Validates that a song was successfully deleted.

    Args:
       result: Result from the database deletion operation.

    Raises:
       SongDeleteException: If no song was deleted.
    """
    if result.deleted_count == 0:
        raise SongDeleteException
