"""
Validations for Blob Song service
"""

from app.exceptions.base_exceptions_schema import BadParameterException
from app.spotify_electron.song.base_song_schema import SongCreateException
from app.spotify_electron.utils.validations.validation_utils import validate_parameter


def validate_song_create(result: str) -> None:
    """Checks if the song creating result is valid

    Args:
        result (str): the result of the song creation operation

    Raises:
        SongCreateException: if the song wasn't created correctly
    """
    try:
        validate_parameter(result)
    except (BadParameterException, Exception) as exception:
        raise SongCreateException from exception
