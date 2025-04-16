"""Validations for Serverless function Song service"""

from requests import Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED

from app.logging.logging_constants import (
    LOGGING_SONG_SERVERLESS_SERVICE_VALIDATIONS,
)
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.song.serverless.song_schema import (
    SongCreateSongStreamingError,
    SongDeleteSongStreamingError,
    SongGetUrlStreamingError,
)

song_service_logger = SpotifyElectronLogger(
    LOGGING_SONG_SERVERLESS_SERVICE_VALIDATIONS
).get_logger()


def validate_song_creating_streaming_response(name: str, response: Response) -> None:
    """Validate create streaming song

    Args:
        name: song name
        response: incoming response

    Raises:
        SongCreateSongStreamingError: request failed
    """
    if response.status_code != HTTP_201_CREATED:
        song_service_logger.error(
            f"Error retrieving Streaming url for song {name}\n"
            f"Request Status {response.status_code} with Content {response.content}"
        )
        raise SongCreateSongStreamingError


def validate_get_song_url_streaming_response(name: str, response: Response) -> None:
    """Validate get url streaming song response

    Args:
        name: song name
        response: the incoming response

    Raises:
        SongGetUrlStreamingError: request failed
    """
    if response.status_code != HTTP_200_OK:
        song_service_logger.error(
            f"Error retrieving Streaming url for song {name}\n"
            f"Request Status {response.status_code} with Content {response.content}"
        )
        raise SongGetUrlStreamingError


def validate_song_deleting_streaming_response(name: str, response: Response) -> None:
    """Validate deleting streaming song

    Args:
        name: song name
        response: incoming response

    Raises:
        SongDeleteSongStreamingError: request failed
    """
    if response.status_code != HTTP_202_ACCEPTED:
        song_service_logger.error(
            f"Error retrieving Streaming url for song {name}\n"
            f"Request Status {response.status_code} with Content {response.content}"
        )
        raise SongDeleteSongStreamingError
