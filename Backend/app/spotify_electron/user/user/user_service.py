"""
User service for handling business logic
"""

import app.auth.auth_service as auth_service
import app.spotify_electron.user.base_user_repository as base_user_repository
import app.spotify_electron.user.providers.user_collection_provider as user_collection_provider
import app.spotify_electron.user.user.user_repository as user_repository
import app.spotify_electron.user.validations.base_user_service_validations as base_user_service_validations  # noqa: E501
from app.logging.logging_constants import LOGGING_USER_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.user.base_user_schema import (
    BaseUserAlreadyExistsError,
    BaseUserBadNameError,
)
from app.spotify_electron.user.user.user_schema import (
    BaseUserRepositoryError,
    UserBadNameError,
    UserDTO,
    UserNotFoundError,
    UserServiceError,
    get_user_dto_from_dao,
)
from app.spotify_electron.utils.date.date_utils import get_current_iso8601_date

user_service_logger = SpotifyElectronLogger(LOGGING_USER_SERVICE).get_logger()


def does_user_exists(user_name: str) -> bool:
    """Returns if user exists

    Args:
    ----
        user_name (str): user name

    Returns:
    -------
        bool: if the user exists

    """
    return base_user_repository.check_user_exists(
        user_name, user_collection_provider.get_user_collection()
    )


def get_user(user_name: str) -> UserDTO:
    """Get user from name

    Args:
        user_name (str): the user name

    Raises:
        UserBadNameError: invalid user name
        UserNotFoundError: user not found
        UserServiceError: unexpected error while getting user

    Returns:
        UserDTO: the user
    """
    try:
        base_user_service_validations.validate_user_name_parameter(user_name)
        user = user_repository.get_user(user_name)
        user_dto = get_user_dto_from_dao(user)
    except BaseUserBadNameError as exception:
        user_service_logger.exception(f"Bad User Name Parameter: {user_name}")
        raise UserBadNameError from exception
    except UserNotFoundError as exception:
        user_service_logger.exception(f"User not found: {user_name}")
        raise UserNotFoundError from exception
    except BaseUserRepositoryError as exception:
        user_service_logger.exception(
            f"Unexpected error in User Repository getting user: {user_name}"
        )
        raise UserServiceError from exception
    except Exception as exception:
        user_service_logger.exception(
            f"Unexpected error in User Service getting user: {user_name}"
        )
        raise UserServiceError from exception
    else:
        user_service_logger.info(f"User {user_name} retrieved successfully")
        return user_dto


def create_user(user_name: str, photo: str, password: str) -> None:
    """Create user

    Args:
        user_name (str): user name
        photo (str): user photo
        password (str): user password

    Raises:
        BaseUserAlreadyExistsError: if the user already exists
        UserBadNameError: if the user name is invalid
        UserServiceError: unexpected error while creating user
    """
    try:
        base_user_service_validations.validate_user_name_parameter(user_name)
        base_user_service_validations.validate_user_should_not_exist(user_name)

        date = get_current_iso8601_date()
        photo = photo if "http" in photo else ""
        hashed_password = auth_service.hash_password(password)

        user_repository.create_user(
            name=user_name,
            photo=photo,
            current_date=date,
            password=hashed_password,
        )
        user_service_logger.info(f"User {user_name} created successfully")
    except BaseUserAlreadyExistsError as exception:
        user_service_logger.exception(f"User already exists: {user_name}")
        raise BaseUserAlreadyExistsError from exception
    except BaseUserBadNameError as exception:
        user_service_logger.exception(f"Bad User Name Parameter: {user_name}")
        raise UserBadNameError from exception
    except BaseUserRepositoryError as exception:
        user_service_logger.exception(
            f"Unexpected error in User Repository creating user: {user_name}"
        )
        raise UserServiceError from exception
    except Exception as exception:
        user_service_logger.exception(
            f"Unexpected error in User Service creating user: {user_name}"
        )
        raise UserServiceError from exception


# TODO obtain all users in same query
def get_users(user_names: list[str]) -> list[UserDTO]:
    """Get users from a list of names

    Args:
        user_names (list[str]): the list with the user names to retrieve

    Raises:
        UserServiceError: unexpected error while getting users

    Returns:
        list[User]: the selected users
    """
    try:
        users: list[UserDTO] = []

        for user_name in user_names:
            users.append(get_user(user_name))

    except BaseUserRepositoryError as exception:
        user_service_logger.exception(
            f"Unexpected error in User Repository getting users {user_names}"
        )
        raise UserServiceError from exception
    except Exception as exception:
        user_service_logger.exception(
            f"Unexpected error in User Service getting users {user_names}"
        )
        raise UserServiceError from exception
    else:
        user_service_logger.info(f"Users {user_names} retrieved successfully")
        return users


def search_by_name(name: str) -> list[UserDTO]:
    """Retrieve the users that matchs the name

    Args:
        name (str): name to match

    Raises:
        UserServiceError: unexpected error searching users that match a name

    Returns:
        list[UserDTO]: users that matchs the name
    """
    try:
        matched_items_names = base_user_repository.search_by_name(
            name, user_collection_provider.get_user_collection()
        )

        return get_users(matched_items_names)
    except BaseUserRepositoryError as exception:
        user_service_logger.exception(
            f"Unexpected error in User Repository getting items by name {name}"
        )
        raise UserServiceError from exception
    except Exception as exception:
        user_service_logger.exception(
            f"Unexpected error in User Service getting items by name {name}"
        )
        raise UserServiceError from exception
