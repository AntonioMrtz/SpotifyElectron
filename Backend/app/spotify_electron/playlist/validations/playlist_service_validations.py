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
    """Raises an exception if playlist name parameter is invalid

    Args:
    ----
        name (str): name

    Raises:
    ------
        PlaylistBadNameException: if name parameter is invalid

    """
    try:
        validate_parameter(name)
    except BadParameterException:
        raise PlaylistBadNameException from BadParameterException


def validate_playlist_should_exists(name: str) -> None:
    """Raises an exception if playlist doesnt exists

    Args:
    ----
        name (str): playlist name

    Raises:
    ------
        PlaylistNotFoundException: if playlist doesnt exists

    """
    if not check_playlist_exists(name):
        raise PlaylistNotFoundException


def validate_playlist_should_not_exists(name: str) -> None:
    """Raises an exception if playlist does exists

    Args:
    ----
        name (str): playlist name

    Raises:
    ------
        PlaylistNotFoundException: if playlist exists

    """
    if check_playlist_exists(name):
        raise PlaylistAlreadyExistsException
