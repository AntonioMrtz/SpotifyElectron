"""
API to comunicate with AWS Serverless Function that handles song files in Cloud
"""

from requests import Response, delete, get, post

from app.common.app_schema import AppEnviroment
from app.common.PropertiesManager import PropertiesManager


def get_song(song_name: str) -> Response:
    """Get song from cloud

    Args:
        song_name (str): song name
    """
    response = get(
        f"{getattr(PropertiesManager,AppEnviroment.SERVERLESS_FUNCTION_URL_ENV_NAME)}",
        params={
            "nombre": song_name,
        },
    )
    return response


def create_song(song_name: str, encoded_bytes: str) -> Response:
    """Create song in cloud

    Args:
        song_name (str): song name
        encoded_bytes (str): encoded bytes of song
    """
    request_data_body = {
        "file": encoded_bytes,
    }
    response = post(
        f"{getattr(PropertiesManager,AppEnviroment.SERVERLESS_FUNCTION_URL_ENV_NAME)}",
        json=request_data_body,
        params={"nombre": song_name},
    )
    return response


def delete_song(song_name: str) -> Response:
    """Delete song from cloud

    Args:
        song_name (str): song name
    """
    response = delete(
        f"{getattr(PropertiesManager,AppEnviroment.SERVERLESS_FUNCTION_URL_ENV_NAME)}",
        params={
            "nombre": song_name,
        },
    )
    return response
