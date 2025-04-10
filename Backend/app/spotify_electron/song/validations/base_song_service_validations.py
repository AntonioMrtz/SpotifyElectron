"""
Common validations for all Song respositories, regardless of the current architecture
"""

from app.exceptions.base_exceptions_schema import BadParameterError
from app.spotify_electron.song.base_song_repository import check_song_exists
from app.spotify_electron.song.base_song_schema import (
    SongAlreadyExistsError,
    SongBadNameError,
    SongNotFoundError,
)
from app.spotify_electron.utils.validations.validation_utils import validate_parameter


def validate_song_name_parameter(name: str) -> None:
    """Raises an exception if song name parameter is invalid

    Args:
        name (str): song name

    Raises:
        SongBadNameError: if name parameter is invalid
    """
    try:
        validate_parameter(name)
    except BadParameterError:
        raise SongBadNameError from BadParameterError


def validate_song_should_exists(name: str) -> None:
    """Raises an exception if song doesn't exists

    Args:
    ----
        name (str): song name

    Raises:
    ------
        SongNotFoundError: if song doesn't exists

    """
    if not check_song_exists(name):
        raise SongNotFoundError


def validate_song_should_not_exists(name: str) -> None:
    """Raises an exception if song does exists

    Args:
    ----
        name (str): song name

    Raises:
    ------
        SongAlreadyExistsError: if song exists

    """
    if check_song_exists(name):
        raise SongAlreadyExistsError
