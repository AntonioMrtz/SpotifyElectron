"""
Validations for Playlist repository
"""

from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from app.spotify_electron.playlist.playlist_schema import (
    PlaylistCreateError,
    PlaylistDAO,
    PlaylistDeleteError,
    PlaylistNotFoundError,
    PlaylistUpdateError,
)


def validate_playlist_exists(playlist: PlaylistDAO | None) -> None:
    """Raises an exception if playlist doesn't exists

    Args:
        playlist (PlaylistDAO | None): the playlist

    Raises:
        PlaylistNotFoundError: if the playlists doesn't exists

    """
    if playlist is None:
        raise PlaylistNotFoundError


def validate_playlist_delete_count(result: DeleteResult) -> None:
    """Raises an exception if playlist deletion count was 0

    Args:
        result (DeleteResult): the result from the deletion

    Raises:
        PlaylistDeleteError: if the deletion was not done

    """
    if result.deleted_count == 0:
        raise PlaylistDeleteError


def validate_playlist_update(result: UpdateResult) -> None:
    """Raises an exception if playlist update was not done

    Args:
        result (UpdateResult): update result

    Raises:
        PlaylistUpdateError: if the update was not done
    """
    if not result.acknowledged:
        raise PlaylistUpdateError


def validate_playlist_create(result: InsertOneResult) -> None:
    """Raises an exception if playlist insertion was not done

    Args:
        result (InsertOneResult): the result from the insertion

    Raises:
        PlaylistCreateError: if the insertion was not done

    """
    if not result.acknowledged:
        raise PlaylistCreateError
