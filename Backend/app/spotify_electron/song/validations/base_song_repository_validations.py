from pymongo.results import DeleteResult, InsertOneResult

from app.spotify_electron.song.base_song_schema import (
    BaseSongDAO,
    SongCreateException,
    SongDeleteException,
    SongNotFoundException,
)


def handle_song_exists(song: BaseSongDAO | None) -> None:
    """Raises an exception if song doesnt exists

    Args:
    ----
        song (BaseSongDAO | None): the song

    Raises:
    ------
        SongNotFoundException: if the song doesnt exists

    """
    if song is None:
        raise SongNotFoundException


def handle_song_create(result: InsertOneResult) -> None:
    """Raises an exception if song insertion was not done

    Args:
    ----
        result (InsertOneResult): the result from the insertion

    Raises:
    ------
        SongCreateException: if the insertion was not done

    """
    if not result.acknowledged:
        raise SongCreateException


def handle_song_delete_count(result: DeleteResult) -> None:
    """Raises an exception if song deletion count was 0

    Args:
    ----
        result (DeleteResult): the result from the deletion

    Raises:
    ------
        SongDeleteException: if the deletion was not done

    """
    if result.deleted_count == 0:
        raise SongDeleteException
