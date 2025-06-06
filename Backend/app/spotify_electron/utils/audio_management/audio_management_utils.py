"""Audio management utils"""

import base64
import io

import librosa

from app.exceptions.base_exceptions_schema import SpotifyElectronError
from app.logging.logging_constants import LOGGING_AUDIO_MANAGEMENT_UTILS
from app.logging.logging_schema import SpotifyElectronLogger

audio_management_utils_logger = SpotifyElectronLogger(
    LOGGING_AUDIO_MANAGEMENT_UTILS
).get_logger()


def get_song_duration_seconds(name: str, file: bytes) -> int:
    """Get song duration

    Args:
        name: song name
        file: song file

    Returns:
        the duration in seconds, defaulted to 0 if not a song file
    """
    try:
        audio_data, sample_rate = librosa.load(io.BytesIO(file), sr=None)
        duration = librosa.get_duration(y=audio_data, sr=sample_rate)

    except Exception:
        # If it's not a sound file
        audio_management_utils_logger.warning(
            f"Cannot get song {name} duration, setting duration to default"
        )
        duration = 0

    audio_management_utils_logger.debug(f"Song file {name} has a {duration} seconds duration")
    return int(duration)


def encode_file(name: str, file: bytes) -> str:
    """Encode file into a string

    Args:
        name: file name
        file: file bytes

    Raises:
        EncodingFileError: encoding file

    Returns:
        the encoded str
    """
    # b'ZGF0YSB0byBiZSBlbmNvZGVk'
    try:
        return str(base64.b64encode(file))
    except Exception as exception:
        audio_management_utils_logger.exception(
            f"Song File with name {name} cannot be encoded"
        )
        raise EncodingFileError from exception


class EncodingFileError(SpotifyElectronError):
    """File encoding error"""

    def __init__(self):
        super().__init__("Error encoding file")
