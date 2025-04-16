"""Validations for Common user services"""

import app.spotify_electron.user.artist.artist_service as artist_service
import app.spotify_electron.user.user.user_service as user_service
from app.exceptions.base_exceptions_schema import BadParameterError
from app.spotify_electron.user.base_user_schema import (
    BaseUserAlreadyExistsError,
    BaseUserBadNameError,
    BaseUserNotFoundError,
)
from app.spotify_electron.utils.validations.validation_utils import validate_parameter


async def validate_user_name_parameter(name: str) -> None:
    """Raises an exception if name parameter is invalid

    Args:
        name: name

    Raises:
        BaseUserBadNameError: parameter is invalid
    """
    try:
        validate_parameter(name)
    except BadParameterError:
        raise BaseUserBadNameError from BadParameterError


async def validate_user_should_exists(user_name: str) -> None:
    """Raises an exception if user doesn't exists

    Args:
        user_name: the user name

    Raises:
        BaseUserNotFoundError: user doesn't exists
    """
    result_artist_exists = await artist_service.does_artist_exists(user_name)
    result_user_exists = await user_service.does_user_exists(user_name)

    if not result_user_exists and not result_artist_exists:
        raise BaseUserNotFoundError


async def validate_user_should_not_exist(user_name: str) -> None:
    """Raises an exception if the user exists

    Args:
        user_name: the user name

    Raises:
        BaseUserAlreadyExistsError: user exists
    """
    result_artist_exists = await artist_service.does_artist_exists(user_name)
    result_user_exists = await user_service.does_user_exists(user_name)

    if result_user_exists or result_artist_exists:
        raise BaseUserAlreadyExistsError
