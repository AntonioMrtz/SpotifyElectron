"""
Validations for Playlist service
"""

from app.exceptions.base_exceptions_schema import BadParameterException
from app.spotify_electron.playlist.playlist_repository import check_playlist_exists
from app.spotify_electron.playlist.playlist_schema import (
    PlaylistAlreadyExistsException,
    PlaylistBadNameException,
    PlaylistNotFoundException,
)
from app.spotify_electron.utils.validations.validation_utils import validate_parameter


def validate_playlist_name_parameter(name: str) -> None:
    """Validates a playlist name parameter.

    Args:
       name (str): The name to validate.

    Raises:
       PlaylistBadNameException: If the name parameter is invalid.
    """
    try:
        validate_parameter(name)
    except BadParameterException:
        raise PlaylistBadNameException from BadParameterException


def validate_playlist_should_exists(name: str) -> None:
    """Validates that a playlist exists.

    Args:
       name (str): Name of the playlist to check.

    Raises:
       PlaylistNotFoundException: If a playlist with the given name does not exist.
    """
    if not check_playlist_exists(name):
        raise PlaylistNotFoundException


def validate_playlist_should_not_exists(name: str) -> None:
    """Validates that a playlist does not already exist.

    Args:
       name (str): Name of the playlist to check.

    Raises:
       PlaylistAlreadyExistsException: If a playlist with the given name exists.
    """
    if check_playlist_exists(name):
        raise PlaylistAlreadyExistsException
