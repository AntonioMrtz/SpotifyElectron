"""
Common validations for all Song services, regardless of the current architecture
"""

from pymongo.results import DeleteResult, InsertOneResult

from app.spotify_electron.song.base_song_schema import (
    BaseSongDAO,
    SongCreateError,
    SongDeleteError,
    SongNotFoundError,
)


def validate_song_exists(song: BaseSongDAO | None) -> None:
    """Raises an exception if song doesn't exists

    Args:
    ----
        song (BaseSongDAO | None): the song

    Raises:
    ------
        SongNotFoundError: if the song doesn't exists

    """
    if song is None:
        raise SongNotFoundError


def validate_base_song_create(result: InsertOneResult) -> None:
    """Raises an exception if song insertion was not done

    Args:
    ----
        result (InsertOneResult): the result from the insertion

    Raises:
    ------
        SongCreateError: if the insertion was not done

    """
    if not result.acknowledged:
        raise SongCreateError


def validate_song_delete_count(result: DeleteResult) -> None:
    """Raises an exception if song deletion count was 0

    Args:
    ----
        result (DeleteResult): the result from the deletion

    Raises:
    ------
        SongDeleteError: if the deletion was not done

    """
    if result.deleted_count == 0:
        raise SongDeleteError
