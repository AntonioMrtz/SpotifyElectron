"""
Validations for Blob Song service
"""

from app.exceptions.base_exceptions_schema import BadParameterError
from app.spotify_electron.song.base_song_schema import SongCreateError
from app.spotify_electron.utils.validations.validation_utils import validate_parameter


def validate_song_create(result: str) -> None:
    """Checks if the song creating result is valid

    Args:
        result (str): the result of the song creation operation

    Raises:
        SongCreateError: if the song wasn't created correctly
    """
    try:
        validate_parameter(result)
    except (BadParameterError, Exception) as exception:
        raise SongCreateError from exception
