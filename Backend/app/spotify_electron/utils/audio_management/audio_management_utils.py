"""
Audio management utils
"""

import base64
import io

import librosa

from app.exceptions.base_exceptions_schema import SpotifyElectronException
from app.logging.logging_constants import LOGGING_AUDIO_MANAGEMENT_UTILS
from app.logging.logging_schema import SpotifyElectronLogger

audio_management_utils_logger = SpotifyElectronLogger(
    LOGGING_AUDIO_MANAGEMENT_UTILS
).getLogger()


def get_song_duration_seconds(name: str, file: bytes) -> int:
    """Get song duration

    Args:
        name (str): song name
        file (_type_): song file

    Returns:
        int: the duration in seconds, defaulted to 0 if not a song file
    """
    try:
        audio_data, sample_rate = librosa.load(io.BytesIO(file), sr=None)
        duration = librosa.get_duration(y=audio_data, sr=sample_rate)

    except Exception:
        # If its not a sound file
        audio_management_utils_logger.exception(
            f"Song File with name {name} is not a song, set duration to default"
        )
        duration = 0

    audio_management_utils_logger.debug(f"Song file {name} has a {duration} seconds duration")
    return int(duration)


def encode_file(name: str, file: bytes) -> str:
    """Encode file into a string

    Args:
        name (str): file name
        file (bytes): file bytes

    Raises:
        EncodingFileException: unexpected error encoding file

    Returns:
        str: the encoded str
    """
    # b'ZGF0YSB0byBiZSBlbmNvZGVk'
    try:
        return str(base64.b64encode(file))
    except Exception:
        audio_management_utils_logger.exception(
            f"Song File with name {name} cannot be encoded"
        )
        raise EncodingFileException


class EncodingFileException(SpotifyElectronException):
    """Exception for Unexpected errors encoding files"""

    def __init__(self):
        super().__init__("Error encoding file")
