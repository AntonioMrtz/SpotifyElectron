"""
Validations for Common user services
"""

import app.spotify_electron.user.artist.artist_service as artist_service
import app.spotify_electron.user.user.user_service as user_service
from app.exceptions.base_exceptions_schema import BadParameterException
from app.spotify_electron.user.base_user_schema import (
    BaseUserAlreadyExistsException,
    BaseUserBadNameException,
    BaseUserNotFoundException,
)
from app.spotify_electron.utils.validations.validation_utils import validate_parameter


def validate_user_name_parameter(name: str) -> None:
    """Raises an exception if name parameter is invalid

    Args:
    ----
        name (str): name

    Raises:
    ------
        BaseUserBadNameException: if name parameter is invalid

    """
    try:
        validate_parameter(name)
    except BadParameterException:
        raise BaseUserBadNameException from BadParameterException


def validate_user_should_exists(user_name: str) -> None:
    """Raises an exception if user doesn't exists

    Args:
        user_name (str): the user name

    Raises:
        BaseUserNotFoundException: if the user doesn't exists
    """
    result_artist_exists = artist_service.does_artist_exists(user_name)
    result_user_exists = user_service.does_user_exists(user_name)

    if not result_user_exists and not result_artist_exists:
        raise BaseUserNotFoundException


def validate_user_should_not_exist(user_name: str) -> None:
    """Raises an exception if the user exists

    Args:
        user_name (str): the user name

    Raises:
        BaseUserAlreadyExistsException: if the user exists
    """
    result_artist_exists = artist_service.does_artist_exists(user_name)
    result_user_exists = user_service.does_user_exists(user_name)

    if result_user_exists or result_artist_exists:
        raise BaseUserAlreadyExistsException
