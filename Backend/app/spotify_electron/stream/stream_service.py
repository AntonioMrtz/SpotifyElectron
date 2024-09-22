"""Stream service for handling business logic"""

from collections.abc import AsyncGenerator

import app.spotify_electron.song.blob.song_service as song_service
from app.logging.logging_constants import LOGGING_STREAM_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.song.base_song_schema import (
    SongBadNameException,
    SongNotFoundException,
    SongRepositoryException,
)
from app.spotify_electron.song.blob.song_schema import SongDataNotFoundException
from app.spotify_electron.stream.stream_constants import SONG_STREAMING_BUFFER_SIZE
from app.spotify_electron.stream.stream_schema import (
    InvalidContentRangeStreamException,
    StreamAudioContent,
    StreamServiceException,
)

stream_service_logger = SpotifyElectronLogger(LOGGING_STREAM_SERVICE).getLogger()


async def stream_audio(song_data: bytes, start: int, end: int) -> AsyncGenerator[bytes, None]:
    """Yield chunks of song data from start to end

    Args:
        song_data (bytes): song data
        start (int): start byte
        end (int): end byte

    Yields:
        AsyncGenerator[bytes, None]: yield chunk bytes from requested range
    """
    # Ensure we don't exceed the end limit
    effective_end = min(end, len(song_data))

    for i in range(start, effective_end, SONG_STREAMING_BUFFER_SIZE):
        yield song_data[i : i + SONG_STREAMING_BUFFER_SIZE]


def _get_range_header(range_header: str | None, file_size: int) -> tuple[int, int]:
    """Get range headers

    Args:
        range_header (str | None): range content header [bytes 1000-1499/1500]
        file_size (int): file size

    Raises:
        InvalidContentRangeStreamException: invalid content range for streaming

    Returns:
        tuple[int, int]: start, end byte position
    """
    try:
        if range_header is None:
            raise InvalidContentRangeStreamException
        h = range_header.replace("bytes=", "").split("-")
        start = int(h[0]) if h[0] != "" else 0
        end = int(h[1]) if h[1] != "" else file_size - 1
    except ValueError:
        raise InvalidContentRangeStreamException

    if start > end or start < 0 or end > file_size - 1:
        raise InvalidContentRangeStreamException
    return start, end


def get_stream_audio_data(range_header: str | None, name: str) -> StreamAudioContent:
    """Gets stream audio data

    Args:
        range_header (str | None): range content header [bytes 1000-1499/1500]
        name (str): song name

    Raises:
        SongBadNameException: invalid song name
        SongNotFoundException: song not found
        SongDataNotFoundException: song data doesn't exists
        InvalidContentRangeStreamException: invalid content range for streaming
        StreamServiceException: unexpected error while getting stream audio data

    Returns:
        StreamAudioContent: the needed audio data for streaming
    """
    try:
        song_data = song_service.get_song_data(name)
        file_size = len(song_data)
        stream_service_logger.info(f"Streaming song {name}")

        headers = {
            "content-type": "audio/mp3",
            "accept-ranges": "bytes",
            "content-encoding": "identity",
            "access-control-expose-headers": (
                "Content-type, Accept-ranges, Content-length, "
                "Content-range, Content-encoding"
            ),
        }

        start, end = _get_range_header(range_header, file_size)
        size = end - start + 1
        headers["Content-length"] = str(size)
        headers["Content-range"] = f"bytes {start}-{end}/{file_size}"

        return StreamAudioContent(song_data=song_data, headers=headers, start=start, end=end)
    except SongBadNameException as exception:
        stream_service_logger.exception(f"Bad Song Name Parameter: {name}")
        raise SongBadNameException from exception
    except SongNotFoundException as exception:
        stream_service_logger.exception(f"Song not found: {name}")
        raise SongNotFoundException from exception
    except SongDataNotFoundException as exception:
        stream_service_logger.exception(f"Song data not found: {name}")
        raise SongDataNotFoundException from exception
    except InvalidContentRangeStreamException as exception:
        stream_service_logger.exception(
            f"Invalid content range {range_header} for song {name}"
        )
        raise InvalidContentRangeStreamException from exception
    except SongRepositoryException as exception:
        stream_service_logger.exception(
            f"Unexpected error in Song Repository getting song data: {name}"
        )
        raise StreamServiceException from exception
    except Exception as exception:
        stream_service_logger.exception(
            f"Unexpected error in Stream Service streaming song: {name}"
        )
        raise StreamServiceException from exception
