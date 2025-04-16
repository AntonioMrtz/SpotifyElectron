"""API to comunicate with Serverless function that handles song files in Cloud"""

from requests import Response, delete, get, post

from app.common.app_schema import AppEnvironment
from app.common.PropertiesManager import PropertiesManager


def get_song(song_name: str) -> Response:
    """Get song from cloud

    Args:
        song_name: song name

    Returns:
        request response
    """
    response = get(
        f"{getattr(PropertiesManager, AppEnvironment.SERVERLESS_URL_ENV_NAME)}",
        params={
            "nombre": song_name,
        },
    )
    return response


def create_song(song_name: str, encoded_bytes: str) -> Response:
    """Create song in cloud

    Args:
        song_name: song name
        encoded_bytes: encoded bytes of song

    Returns:
        request response
    """
    request_data_body = {
        "file": encoded_bytes,
    }
    response = post(
        f"{getattr(PropertiesManager, AppEnvironment.SERVERLESS_URL_ENV_NAME)}",
        json=request_data_body,
        params={"nombre": song_name},
    )
    return response


def delete_song(song_name: str) -> Response:
    """Delete song from cloud

    Args:
        song_name: song name

    Returns:
        request response
    """
    response = delete(
        f"{getattr(PropertiesManager, AppEnvironment.SERVERLESS_URL_ENV_NAME)}",
        params={
            "nombre": song_name,
        },
    )
    return response
