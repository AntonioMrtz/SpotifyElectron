"""
User service for handling business logic
"""

from asyncio import gather

import app.auth.auth_service as auth_service
import app.auth.auth_service_validations as auth_service_validations
import app.spotify_electron.user.artist.artist_service as artist_service
import app.spotify_electron.user.base_user_repository as base_user_repository
import app.spotify_electron.user.providers.user_collection_provider as user_collection_provider
import app.spotify_electron.user.user.user_repository as user_repository
import app.spotify_electron.user.validations.base_user_service_validations as base_user_service_validations  # noqa: E501
from app.auth.auth_schema import TokenData, UserUnauthorizedError
from app.logging.logging_constants import LOGGING_USER_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.user.artist.artist_schema import (
    ArtistAlreadyExistsError,
    ArtistServiceError,
)
from app.spotify_electron.user.base_user_schema import (
    BaseUserAlreadyExistsError,
    BaseUserBadNameError,
    BaseUserNotFoundError,
    BaseUserRepositoryError,
)
from app.spotify_electron.user.user.user_schema import (
    UserBadNameError,
    UserDTO,
    UserNotFoundError,
    UserServiceError,
    get_user_dto_from_dao,
)
from app.spotify_electron.utils.date.date_utils import get_current_iso8601_date

user_service_logger = SpotifyElectronLogger(LOGGING_USER_SERVICE).get_logger()


async def does_user_exists(user_name: str) -> bool:
    """Returns if user exists

    Args:
        user_name (str): user name

    Returns:
        bool: if the user exists
    """
    collection = user_collection_provider.get_user_collection()
    return await base_user_repository.check_user_exists(user_name, collection)


async def get_user(user_name: str) -> UserDTO:
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
        await base_user_service_validations.validate_user_name_parameter(user_name)
        user = await user_repository.get_user(user_name)
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


async def create_user(user_name: str, photo: str, password: str) -> None:
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
        await base_user_service_validations.validate_user_name_parameter(user_name)
        await base_user_service_validations.validate_user_should_not_exist(user_name)

        date = get_current_iso8601_date()
        photo = photo if "http" in photo else ""
        hashed_password = auth_service.hash_password(password)

        await user_repository.create_user(
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
async def get_users(user_names: list[str]) -> list[UserDTO]:
    """Get users from a list of names

    Args:
        user_names (list[str]): the list with the user names to retrieve

    Raises:
        UserServiceError: unexpected error while getting users

    Returns:
        list[User]: the selected users
    """
    try:
        users = await gather(*[get_user(name) for name in user_names])

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


async def search_by_name(name: str) -> list[UserDTO]:
    """Retrieve the users that match the name

    Args:
        name (str): name to match

    Raises:
        UserServiceError: unexpected error searching users that match a name

    Returns:
        list[UserDTO]: users that match the name
    """
    try:
        user_collection = user_collection_provider.get_user_collection()
        matched_items_names = await base_user_repository.search_by_name(name, user_collection)

        return await get_users(matched_items_names)
    except BaseUserRepositoryError as exception:
        user_service_logger.exception(
            f"Unexpected error in User Repository getting items by name {name}"
        )
        raise UserServiceError from exception


async def promote_user_to_artist(name: str, token: TokenData) -> None:
    """Promote user to artist

    Args:
        name (str): Username of the user to be promoted
        token (TokenData): Token containing user authentication and authorization data

    Raises:
        ArtistAlreadyExistsError: If an artist with the given name already exists
        UserBadNameError: If the provided username is invalid
        UserUnauthorizedError: If the user lacks required permissions
        UserNotFoundError: If no user exists with the given name
        UserServiceError: If an unexpected error occurs during promotion process
    """
    try:
        # TODO: Make this a transaction. Currently it's transaction-like.
        await base_user_service_validations.validate_user_name_parameter(name)
        await base_user_service_validations.validate_user_should_exists(name)
        auth_service_validations.validate_jwt_user_matches_user(token, name)

        user = await user_repository.get_user(name)
        await artist_service.create_artist_from_user(user)

        user_collection = user_collection_provider.get_user_collection()
        await base_user_repository.delete_user(user.name, user_collection)
    except ArtistAlreadyExistsError as exception:
        user_service_logger.exception(f"Artist already exists: {name}")
        raise ArtistAlreadyExistsError from exception
    except BaseUserBadNameError as exception:
        user_service_logger.exception(f"Bad parameters for user: {name}")
        raise UserBadNameError from exception
    except UserUnauthorizedError as exception:
        user_service_logger.exception(
            f"Unauthorized user {token.username} with role {token.role} "
            f"trying to promote user {name}"
        )
        raise UserUnauthorizedError from exception
    except BaseUserNotFoundError as exception:
        user_service_logger.exception(f"User not found: {name}")
        raise UserNotFoundError from exception
    except BaseUserRepositoryError as exception:
        user_service_logger.exception(
            f"Unexpected error in User Repository promoting user: {name}"
        )
        raise UserServiceError from exception
    except ArtistServiceError as exception:
        artist_service.artist_service_logger.exception(
            f"Artist creation from User {name} failed"
        )
        raise UserServiceError from exception
    except Exception as exception:
        user_service_logger.exception(
            f"Unexpected error in User Service promoting user: {name}"
        )
        raise UserServiceError from exception
    else:
        user_service_logger.info(f"User: {user.name} promoted to artist successfully")
