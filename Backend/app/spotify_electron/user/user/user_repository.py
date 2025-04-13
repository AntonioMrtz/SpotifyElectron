"""
User repository for managing persisted data
"""

import app.spotify_electron.user.providers.user_collection_provider as provider
from app.logging.logging_constants import LOGGING_USER_REPOSITORY
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.user.base_user_schema import (
    BaseUserCreateError,
    BaseUserNotFoundError,
)
from app.spotify_electron.user.user.user_schema import (
    UserDAO,
    UserDocument,
    UserNotFoundError,
    UserRepositoryError,
    get_user_dao_from_document,
)
from app.spotify_electron.user.validations.base_user_repository_validations import (
    validate_user_create,
    validate_user_exists,
)

user_repository_logger = SpotifyElectronLogger(LOGGING_USER_REPOSITORY).get_logger()


async def get_user(name: str) -> UserDAO:
    """Get user by name

    Args:
        name (str): user name

    Raises:
        UserNotFoundError: user was not found
        UserRepositoryError: unexpected error while getting user

    Returns:
        UserDAO: the user
    """
    try:
        collection = provider.get_user_collection()
        user = await collection.find_one({"name": name})

        validate_user_exists(user)
        assert user

        user_dao = get_user_dao_from_document(user)

    except BaseUserNotFoundError as exception:
        raise UserNotFoundError from exception

    except Exception as exception:
        user_repository_logger.exception(f"Error getting User {name} from database")
        raise UserRepositoryError from exception
    else:
        user_repository_logger.info(f"Get User by name returned {user_dao}")
        return user_dao


async def create_user(name: str, photo: str, password: bytes, current_date: str) -> None:
    """Create user

    Args:
        name (str): user name
        photo (str): user photo
        password (bytes): user hashed password
        current_date (str): formatted creation date

    Raises:
        UserRepositoryError: unexpected error while creating user
    """
    try:
        user: UserDocument = {
            "name": name,
            "photo": photo,
            "register_date": current_date,
            "password": password,
            "saved_playlists": [],
            "playlists": [],
            "playback_history": [],
        }
        collection = provider.get_user_collection()
        result = await collection.insert_one(user)

        validate_user_create(result)
    except BaseUserCreateError as exception:
        user_repository_logger.exception(f"Error inserting User {user} in database")
        raise UserRepositoryError from exception
    except (UserRepositoryError, Exception) as exception:
        user_repository_logger.exception(f"Unexpected error inserting user {user} in database")
        raise UserRepositoryError from exception
    else:
        user_repository_logger.info(f"User added to repository: {user}")
