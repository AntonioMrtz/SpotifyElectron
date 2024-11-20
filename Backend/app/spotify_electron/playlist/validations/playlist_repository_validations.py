"""
Validations for Playlist repository
"""

from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from app.spotify_electron.playlist.playlist_schema import (
    PlaylistCreateException,
    PlaylistDAO,
    PlaylistDeleteException,
    PlaylistNotFoundException,
    PlaylistUpdateException,
)


def validate_playlist_exists(playlist: PlaylistDAO | None) -> None:
    """Validates that a playlist exists.

    Args:
       playlist: The playlist to validate.

    Raises:
       PlaylistNotFoundException: If the playlist is None.
    """
    if playlist is None:
        raise PlaylistNotFoundException


def validate_playlist_delete_count(result: DeleteResult) -> None:
    """Validates that a playlist was successfully deleted.

    Args:
       result: Result from the database deletion operation.

    Raises:
       PlaylistDeleteException: If no playlist was deleted.
    """
    if result.deleted_count == 0:
        raise PlaylistDeleteException


def validate_playlist_update(result: UpdateResult) -> None:
    """Raises an exception if playlist update was not done

    Args:
        result (UpdateResult): update result

    Raises:
        PlaylistUpdateException: if the update was not done
    """
    if not result.acknowledged:
        raise PlaylistUpdateException


def validate_playlist_create(result: InsertOneResult) -> None:
    """Validates that a playlist was successfully created.

    Args:
       result: Result from the database insertion operation.

    Raises:
       PlaylistCreateException: If the playlist insertion was not acknowledged.
    """
    if not result.acknowledged:
        raise PlaylistCreateException
