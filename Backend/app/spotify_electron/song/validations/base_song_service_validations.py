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
    """Raises an exception if song doesnt exists

    Args:
    ----
        name (str): song name

    Raises:
    ------
        SongNotFoundException: if song doesnt exists

    """
    if not check_song_exists(name):
        raise SongNotFoundException


def validate_song_should_not_exists(name: str) -> None:
    """Raises an exception if song does exists

    Args:
    ----
        name (str): song name

    Raises:
    ------
        SongAlreadyExistsException: if song exists

    """
    if check_song_exists(name):
        raise SongAlreadyExistsException
