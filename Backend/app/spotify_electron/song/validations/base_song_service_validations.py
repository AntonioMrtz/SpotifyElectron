"""
Common validations for all Song respositories, regardless of the current architecture
"""

from app.exceptions.base_exceptions_schema import BadParameterException
from app.spotify_electron.song.base_song_repository import check_song_exists
from app.spotify_electron.song.base_song_schema import (
    SongAlreadyExistsException,
    SongBadNameException,
    SongNotFoundException,
)
from app.spotify_electron.utils.validations.validation_utils import validate_parameter


def validate_song_name_parameter(name: str) -> None:
    """Raises an exception if song name parameter is invalid

    Args:
        name (str): song name

    Raises:
        SongBadNameException: if name parameter is invalid
    """
    try:
        validate_parameter(name)
    except BadParameterException:
        raise SongBadNameException from BadParameterException


def validate_song_should_exists(name: str) -> None:
    """Validates that a song exists.

    Args:
       name: Name of the song to check.

    Raises:
       SongNotFoundException: If a song with the given name does not exist.
    """
    if not check_song_exists(name):
        raise SongNotFoundException


def validate_song_should_not_exists(name: str) -> None:
    """Validates that a song does not already exist.

    Args:
       name: Name of the song to check.

    Raises:
       SongAlreadyExistsException: If a song with the given name exists.
    """
    if check_song_exists(name):
        raise SongAlreadyExistsException
