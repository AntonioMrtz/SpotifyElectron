"""
User repository for persisted data.
It uses the collection for the associated user type
"""

from pymongo.collection import Collection

from app.logging.logging_constants import LOGGING_BASE_USERS_REPOSITORY
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.user.user.user_schema import (
    UserDeleteException,
    UserGetPasswordException,
    UserRepositoryException,
)
from app.spotify_electron.user.validations.base_user_repository_validations import (
    validate_password_exists,
    validate_user_delete_count,
)

base_user_repository_logger = SpotifyElectronLogger(LOGGING_BASE_USERS_REPOSITORY).getLogger()


def check_user_exists(name: str, collection: Collection) -> bool:
    """Checks if user exists

    Args:
    ----
        name (str): name of the user

    Raises:
    ------
        UserRepositoryException: an error occurred while getting user from database

    Returns:
    -------
        bool: if the user exsists

    """
    try:
        user = collection.find_one({"name": name}, {"_id": 0, "name": 1})
    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error checking if User {name} exists in database"
        )
        raise UserRepositoryException from exception
    else:
        result = user is not None
        base_user_repository_logger.debug(f"User with name {name} exists: {result}")
        return result


def delete_user(name: str, collection: Collection) -> None:
    """Delete user

    Args:
        name (str): user name

    Raises:
        UserRepositoryException: an error occurred while deleting user from database
    """
    try:
        result = collection.delete_one({"name": name})
        validate_user_delete_count(result)
        base_user_repository_logger.info(f"User {name} Deleted")
    except UserDeleteException as exception:
        base_user_repository_logger.exception(f"Error deleting User {name} from database")
        raise UserRepositoryException from exception
    except (UserRepositoryException, Exception) as exception:
        base_user_repository_logger.exception(
            f"Unexpected error deleting User {name} in database"
        )
        raise UserRepositoryException from exception


def get_user_password(name: str, collection: Collection) -> bytes:
    """Get password from user

    Args:
        name (str): user name
        collection (Collection): the database collection

    Raises:
        UserRepositoryException: an error occurred while getting user password from database

    Returns:
        bytes: the user password
    """
    try:
        password = collection.find_one({"name": name}, {"password": 1, "_id": 0})[  # type: ignore
            "password"
        ]
        validate_password_exists(password)
    except UserGetPasswordException as exception:
        base_user_repository_logger.exception(
            f"Error getting password from User {name} from database"
        )
        raise UserRepositoryException from exception
    except (UserRepositoryException, Exception) as exception:
        base_user_repository_logger.exception(
            f"Unexpected error getting password from User {name} in database"
        )
        raise UserRepositoryException from exception
    else:
        return password


def search_by_name(name: str, collection: Collection) -> list[str]:
    """Get user items that matches a name

    Args:
        name (str): name to match
        collection (Collection): user collection

    Raises:
        UserRepositoryException: unexpected error searching items by name

    Returns:
        list[str]: the list of user names that matched the name
    """
    try:
        matching_items = collection.find(
            {"name": {"$regex": name, "$options": "i"}}, {"_id": 0, "name": 1}
        )
        return [user["name"] for user in matching_items]
    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error checking searching items by name {name} in database"
        )
        raise UserRepositoryException from exception


def add_stream_history(
    user_name: str,
    song: str,
    max_number_stream_history_songs: int,
    collection: Collection,
) -> None:
    """Add song stream history to user

    Args:
        user_name (str): user name
        song (str): song name
        max_number_stream_history_songs (int): max number of songs stored in stream history
        collection (Collection): the user collection

    Raises:
        UserRepositoryException: unexpected error adding song to user stream history
    """
    try:
        user_data = collection.find_one({"name": user_name})

        stream_history = user_data["stream_history"]  # type: ignore

        if len(stream_history) == max_number_stream_history_songs:
            stream_history.pop(0)

        stream_history.append(song)

        collection.update_one(
            {"name": user_name}, {"$set": {"stream_history": stream_history}}
        )
    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error adding stream history of song {song} to user {user_name} in database"
        )
        raise UserRepositoryException from exception


def add_saved_playlist(user_name: str, playlist_name: str, collection: Collection) -> None:
    """Add saved playlist to user

    Args:
        user_name (str): user name
        playlist_name (str): playlist name
        collection (Collection): user collection

    Raises:
        UserRepositoryException: unexpected error adding saved playlist to user
    """
    try:
        # TODO make in one query
        user_data = collection.find_one({"name": user_name})
        saved_playlists = user_data["saved_playlists"]  # type: ignore

        saved_playlists.append(playlist_name)

        collection.update_one(
            {"name": user_name},
            {"$set": {"saved_playlists": list(set(saved_playlists))}},
        )
    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error adding playlist {playlist_name} "
            f"to user {user_name} saved playlists in database"
        )
        raise UserRepositoryException from exception


def delete_saved_playlist(user_name: str, playlist_name: str, collection: Collection) -> None:
    """Deletes a saved playlist from a user

    Args:
        user_name (str): user name
        playlist_name (str): playlist name
        collection (Collection): user collection

    Raises:
        UserRepositoryException: unexpected error deleting saved playlist from user
    """
    try:
        user_data = collection.find_one({"name": user_name})

        saved_playlists = user_data["saved_playlists"]  # type: ignore

        if playlist_name in saved_playlists:
            saved_playlists.remove(playlist_name)

            collection.update_one(
                {"name": user_name}, {"$set": {"saved_playlists": saved_playlists}}
            )
    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error deleting saved playlist {playlist_name} from user {user_name} in database"
        )
        raise UserRepositoryException from exception


def add_playlist_to_owner(user_name: str, playlist_name: str, collection: Collection) -> None:
    """Adds a playlist to his ownwer

    Args:
        user_name (str): owner name
        playlist_name (str): playlist name
        collection (Collection): user collection

    Raises:
        UserRepositoryException: unexpected error adding playlist to its owner
    """
    try:
        user_data = collection.find_one({"name": user_name})

        playlists = user_data["playlists"]  # type: ignore

        playlists.append(playlist_name)

        collection.update_one(
            {"name": user_name}, {"$set": {"playlists": list(set(playlists))}}
        )

    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error adding playlist {playlist_name} to owner {user_name} in database"
        )
        raise UserRepositoryException from exception


def delete_playlist_from_owner(
    user_name: str, playlist_name: str, collection: Collection
) -> None:
    """Deletes a playlist from his ownwer

    Args:
        user_name (str): owner name
        playlist_name (str): playlist name
        collection (Collection): user collection

    Raises:
        UserRepositoryException: unexpected error deleting playlist from owner
    """
    try:
        user_data = collection.find_one({"name": user_name})

        playlists = user_data["playlists"]  # type: ignore

        if playlist_name in playlists:
            playlists.remove(playlist_name)

            collection.update_one({"name": user_name}, {"$set": {"playlists": playlists}})
    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error deleting playlist {playlist_name} from owner {user_name} in database"
        )
        raise UserRepositoryException from exception


def update_playlist_name(
    old_playlist_name: str, new_playlist_name: str, collection: Collection
) -> None:
    """Update playlist name with a new one

    Args:
        old_playlist_name (str): old name
        new_playlist_name (str): new name
        collection (Collection): user collection

    Raises:
        UserRepositoryException: unexpected error updating playlist name
    """
    try:
        # has to be done sequentially, pull and push on the same query generates errors
        collection.update_many(
            {"saved_playlists": old_playlist_name},
            {"$set": {"saved_playlists.$": new_playlist_name}},
        )
        collection.update_many(
            {"playlists": old_playlist_name},
            {"$set": {"playlists.$": new_playlist_name}},
        )

    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error updating playlist name {old_playlist_name} "
            f"to {new_playlist_name} in database"
        )
        raise UserRepositoryException from exception


def get_user_relevant_playlist_names(user_name: str, collection: Collection) -> list[str]:
    """Get user relevant playlist names

    Args:
        user_name (str): user name
        collection (Collection): user collection

    Returns:
        list[str]: the playlist names of the playlists relevant to the user
    """
    user_data = collection.find_one(
        {"name": user_name}, {"playlists": 1, "saved_playlists": 1, "_id": 0}
    )
    playlist_names = []
    playlist_names.extend(user_data["playlists"])  # type: ignore
    playlist_names.extend(user_data["saved_playlists"])  # type: ignore

    return playlist_names


def get_user_playlist_names(user_name: str, collection: Collection) -> list[str]:
    """Get user created playlist names

    Args:
        user_name (str): user name
        collection (Collection): user collection

    Returns:
        list[str]: the playlist names of the user created playlists
    """
    user_data = collection.find_one({"name": user_name}, {"playlists": 1, "_id": 0})

    return user_data["playlists"]  # type: ignore


def get_user_stream_history_names(user_name: str, collection: Collection) -> list[str]:
    """Get user stream history song names

    Args:
        user_name (str): user name
        collection (Collection): user collection

    Returns:
        list[str]: the user stream history
    """
    user_data = collection.find_one({"name": user_name}, {"stream_history": 1, "_id": 0})

    return user_data["stream_history"]  # type: ignore
