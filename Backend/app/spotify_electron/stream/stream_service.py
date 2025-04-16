"""Stream service for handling business logic

Based on: https://github.com/fastapi/fastapi/issues/1240#issuecomment-1312294359
"""

from collections.abc import AsyncGenerator

import app.spotify_electron.song.blob.song_service as song_service
from app.logging.logging_constants import LOGGING_STREAM_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.song.base_song_schema import (
    SongBadNameError,
    SongNotFoundError,
    SongRepositoryError,
)
from app.spotify_electron.song.blob.song_schema import SongDataNotFoundError
from app.spotify_electron.stream.stream_constants import SONG_STREAMING_BUFFER_SIZE
from app.spotify_electron.stream.stream_schema import (
    InvalidContentRangeStreamError,
    StreamAudioContent,
    StreamServiceError,
)

stream_service_logger = SpotifyElectronLogger(LOGGING_STREAM_SERVICE).get_logger()


async def stream_audio(song_data: bytes, start: int, end: int) -> AsyncGenerator[bytes, None]:
    """Yield chunks of song data from start to end

    Args:
        song_data: song data
        start: start byte
        end: end byte

    Yields:
        yield chunk bytes from requested range
    """
    # Ensure we don't exceed the end limit
    effective_end = min(end, len(song_data))

    for i in range(start, effective_end, SONG_STREAMING_BUFFER_SIZE):
        yield song_data[i : i + SONG_STREAMING_BUFFER_SIZE]


def _get_range_header(range_header: str | None, file_size: int) -> tuple[int, int]:
    """Get range headers

    Args:
        range_header: range content header [bytes 1000-1499/1500]
        file_size: file size

    Raises:
        InvalidContentRangeStreamError: range for streaming

    Returns:
        start, end byte position
    """
    try:
        if range_header is None:
            raise InvalidContentRangeStreamError
        h = range_header.replace("bytes=", "").split("-")
        start = int(h[0]) if h[0] != "" else 0
        end = int(h[1]) if h[1] != "" else file_size - 1
    except ValueError as exception:
        raise InvalidContentRangeStreamError from exception

    if start > end or start < 0 or end > file_size - 1:
        raise InvalidContentRangeStreamError
    return start, end


async def get_stream_audio_data(range_header: str | None, name: str) -> StreamAudioContent:
    """Gets stream audio data

    Args:
        range_header: range content header [bytes 1000-1499/1500]\
         https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests
        name: song name

    Raises:
        SongBadNameError: name
        SongNotFoundError: song not found
        SongDataNotFoundError: song data doesn't exists
        InvalidContentRangeStreamError: invalid content range for streaming
        StreamServiceError: unexpected error while getting stream audio data

    Returns:
        the needed audio data for streaming
    """
    try:
        song_data = await song_service.get_song_data(name)
        file_size = len(song_data)
        stream_service_logger.info(f"Streaming song {name}")

        headers = {
            "content-type": "audio/mp3",
            "accept-ranges": "bytes",
            "content-encoding": "identity",
            "access-control-expose-headers": (
                "Content-type, Accept-ranges, Content-length, Content-range, Content-encoding"
            ),
        }

        start, end = _get_range_header(range_header, file_size)
        size = end - start + 1
        headers["Content-length"] = str(size)
        headers["Content-range"] = f"bytes {start}-{end}/{file_size}"

        return StreamAudioContent(song_data=song_data, headers=headers, start=start, end=end)
    except SongBadNameError as exception:
        stream_service_logger.exception(f"Bad Song Name Parameter: {name}")
        raise SongBadNameError from exception
    except SongNotFoundError as exception:
        stream_service_logger.exception(f"Song not found: {name}")
        raise SongNotFoundError from exception
    except SongDataNotFoundError as exception:
        stream_service_logger.exception(f"Song data not found: {name}")
        raise SongDataNotFoundError from exception
    except InvalidContentRangeStreamError as exception:
        stream_service_logger.exception(
            f"Invalid content range {range_header} for song {name}"
        )
        raise InvalidContentRangeStreamError from exception
    except SongRepositoryError as exception:
        stream_service_logger.exception(
            f"Unexpected error in Song Repository getting song data: {name}"
        )
        raise StreamServiceError from exception
    except Exception as exception:
        stream_service_logger.exception(
            f"Unexpected error in Stream Service streaming song: {name}"
        )
        raise StreamServiceError from exception
