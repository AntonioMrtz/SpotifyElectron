"""
Validations for AWS Serverless Function Song service
"""

from requests import Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED

from app.logging.logging_constants import (
    LOGGING_SONG_AWS_SERVERLESS_FUNCTION_SERVICE_VALIDATIONS,
)
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.song.aws.serverless_function.song_schema import (
    SongCreateSongStreamingException,
    SongDeleteSongStreamingException,
    SongGetUrlStreamingException,
)

song_service_logger = SpotifyElectronLogger(
    LOGGING_SONG_AWS_SERVERLESS_FUNCTION_SERVICE_VALIDATIONS
).getLogger()


def validate_song_creating_streaming_response(name: str, response: Response) -> None:
    """Validate create streaming song

    Args:
        name (str): song name
        response (Response): incoming response

    Raises:
        SongCreateSongStreamingException: if the request failed
    """
    if response.status_code != HTTP_201_CREATED:
        song_service_logger.error(
            f"Error retrieving Streaming url for song {name}"
            f"Request Status {response.status_code} with Content {response.content}"
        )
        raise SongCreateSongStreamingException


def validate_get_song_url_streaming_response(name: str, response: Response) -> None:
    """Validate get url streaming song response

    Args:
        name (str): song name
        response (Response): the incoming response

    Raises:
        SongGetUrlStreamingException: if the request failed
    """
    if response.status_code != HTTP_200_OK:
        song_service_logger.error(
            f"Error retrieving Streaming url for song {name}"
            f"Request Status {response.status_code} with Content {response.content}"
        )
        raise SongGetUrlStreamingException


def validate_song_deleting_streaming_response(name: str, response: Response) -> None:
    """Validate deleting streaming song

    Args:
        name (str): song name
        response (Response): incoming response

    Raises:
        SongDeleteSongStreamingException: if the request failed
    """
    if response.status_code != HTTP_202_ACCEPTED:
        song_service_logger.error(
            f"Error retrieving Streaming url for song {name}"
            f"Request Status {response.status_code} with Content {response.content}"
        )
        raise SongDeleteSongStreamingException
