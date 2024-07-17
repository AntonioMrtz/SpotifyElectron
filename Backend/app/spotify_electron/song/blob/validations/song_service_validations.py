"""
Validations for Blob Song service
"""

from app.exceptions.base_exceptions_schema import BadParameterException
from app.spotify_electron.song.base_song_schema import SongCreateException
from app.spotify_electron.utils.validations.validation_utils import validate_parameter


def validate_song_create(result: str):
    """Raises an exception of the result of song creation is invalid

    Args:
    ----
        result (str): the result of creating the song

    """
    try:
        validate_parameter(result)
    except (BadParameterException, Exception) as exception:
        raise SongCreateException from exception
