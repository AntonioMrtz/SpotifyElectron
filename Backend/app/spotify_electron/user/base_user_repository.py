"""User repository for persisted data.
It uses the collection for the associated user type
"""

from motor.motor_asyncio import AsyncIOMotorCollection

from app.logging.logging_constants import LOGGING_BASE_USERS_REPOSITORY
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.user.base_user_schema import (
    BaseUserDeleteError,
    BaseUserGetPasswordError,
    BaseUserRepositoryError,
)
from app.spotify_electron.user.validations.base_user_repository_validations import (
    validate_password_exists,
    validate_user_delete_count,
    validate_user_exists,
)

base_user_repository_logger = SpotifyElectronLogger(LOGGING_BASE_USERS_REPOSITORY).get_logger()


async def check_user_exists(name: str, collection: AsyncIOMotorCollection) -> bool:
    """Checks if user exists

    Args:
    ----
        name: name of the user
        collection: user collection

    Raises:
    ------
        BaseUserRepositoryError:
            an error occurred while getting user from database

    Returns:
    -------
        if the user exists
    """
    try:
        user = await collection.find_one({"name": name}, {"_id": 0, "name": 1})
    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error checking if User {name} exists in database"
        )
        raise BaseUserRepositoryError from exception
    else:
        result = user is not None
        base_user_repository_logger.debug(f"User with name {name} exists: {result}")
        return result


async def delete_user(name: str, collection: AsyncIOMotorCollection) -> None:
    """Delete user

    Args:
        name: user name
        collection: user collection

    Raises:
        BaseUserRepositoryError: occurred while deleting user from database"""
    try:
        result = await collection.delete_one({"name": name})
        validate_user_delete_count(result)
        base_user_repository_logger.info(f"User {name} Deleted")
    except BaseUserDeleteError as exception:
        base_user_repository_logger.exception(f"Error deleting User {name} from database")
        raise BaseUserRepositoryError from exception
    except (BaseUserRepositoryError, Exception) as exception:
        base_user_repository_logger.exception(
            f"Unexpected error deleting User {name} in database"
        )
        raise BaseUserRepositoryError from exception


async def get_user_password(name: str, collection: AsyncIOMotorCollection) -> bytes:
    """Get password from user

    Args:
        name: user name
        collection: the database collection

    Raises:
        BaseUserRepositoryError: occurred while getting user password from database

    Returns:
        the user password
    """
    try:
        user_data = await collection.find_one({"name": name}, {"password": 1, "_id": 0})

        validate_user_exists(user_data)
        assert user_data

        password = user_data["password"]
        validate_password_exists(password)
    except BaseUserGetPasswordError as exception:
        base_user_repository_logger.exception(
            f"Error getting password from User {name} from database"
        )
        raise BaseUserRepositoryError from exception
    except (BaseUserRepositoryError, Exception) as exception:
        base_user_repository_logger.exception(
            f"Unexpected error getting password from User {name} in database"
        )
        raise BaseUserRepositoryError from exception
    else:
        return password


async def search_by_name(name: str, collection: AsyncIOMotorCollection) -> list[str]:
    """Get user items that matches a name

    Args:
        name: name to match
        collection: user collection

    Raises:
        BaseUserRepositoryError: searching items by name

    Returns:
        the list of user names that matched the name
    """
    try:
        matching_items = collection.find(
            {"name": {"$regex": name, "$options": "i"}}, {"_id": 0, "name": 1}
        )
        return [user["name"] async for user in matching_items]
    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error checking searching items by name {name} in database"
        )
        raise BaseUserRepositoryError from exception


async def add_playback_history(
    user_name: str,
    song: str,
    max_number_playback_history_songs: int,
    collection: AsyncIOMotorCollection,
) -> None:
    """Add song playback history to user

    Args:
        user_name: user name
        song: song name
        max_number_playback_history_songs: max number of songs stored in playback history
        collection: the user collection

    Raises:
        BaseUserRepositoryError: adding song to user playback history
    """
    try:
        user_data = await collection.find_one({"name": user_name})

        validate_user_exists(user_data)
        assert user_data

        playback_history = user_data["playback_history"]

        if len(playback_history) == max_number_playback_history_songs:
            playback_history.pop(0)

        playback_history.append(song)

        await collection.update_one(
            {"name": user_name}, {"$set": {"playback_history": playback_history}}
        )
    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error adding playback history of song {song} to user {user_name} in database"
        )
        raise BaseUserRepositoryError from exception


async def add_saved_playlist(
    user_name: str, playlist_name: str, collection: AsyncIOMotorCollection
) -> None:
    """Add saved playlist to user

    Args:
        user_name: user name
        playlist_name: playlist name
        collection: user collection

    Raises:
        BaseUserRepositoryError: adding saved playlist to user
    """
    try:
        # TODO make in one query
        user_data = await collection.find_one({"name": user_name})

        validate_user_exists(user_data)
        assert user_data

        saved_playlists = user_data["saved_playlists"]

        saved_playlists.append(playlist_name)

        await collection.update_one(
            {"name": user_name},
            {"$set": {"saved_playlists": list(set(saved_playlists))}},
        )
    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error adding playlist {playlist_name} "
            f"to user {user_name} saved playlists in database"
        )
        raise BaseUserRepositoryError from exception


async def delete_saved_playlist(
    user_name: str, playlist_name: str, collection: AsyncIOMotorCollection
) -> None:
    """Deletes a saved playlist from a user

    Args:
        user_name: user name
        playlist_name: playlist name
        collection: user collection

    Raises:
        BaseUserRepositoryError: deleting saved playlist from user
    """
    try:
        user_data = await collection.find_one({"name": user_name})

        validate_user_exists(user_data)
        assert user_data

        saved_playlists = user_data["saved_playlists"]

        if playlist_name in saved_playlists:
            saved_playlists.remove(playlist_name)

            await collection.update_one(
                {"name": user_name}, {"$set": {"saved_playlists": saved_playlists}}
            )
    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error deleting saved playlist {playlist_name} from user {user_name} in database"
        )
        raise BaseUserRepositoryError from exception


async def add_playlist_to_owner(
    user_name: str, playlist_name: str, collection: AsyncIOMotorCollection
) -> None:
    """Adds a playlist to his ownwer

    Args:
        user_name: owner name
        playlist_name: playlist name
        collection: user collection

    Raises:
        BaseUserRepositoryError: adding playlist to its owner
    """
    try:
        user_data = await collection.find_one({"name": user_name})

        validate_user_exists(user_data)
        assert user_data

        playlists = user_data["playlists"]

        playlists.append(playlist_name)

        await collection.update_one(
            {"name": user_name}, {"$set": {"playlists": list(set(playlists))}}
        )

    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error adding playlist {playlist_name} to owner {user_name} in database"
        )
        raise BaseUserRepositoryError from exception


async def delete_playlist_from_owner(
    user_name: str, playlist_name: str, collection: AsyncIOMotorCollection
) -> None:
    """Deletes a playlist from his ownwer

    Args:
        user_name: owner name
        playlist_name: playlist name
        collection: user collection

    Raises:
        BaseUserRepositoryError: deleting playlist from owner
    """
    try:
        user_data = await collection.find_one({"name": user_name})

        validate_user_exists(user_data)
        assert user_data

        playlists = user_data["playlists"]

        if playlist_name in playlists:
            playlists.remove(playlist_name)

            await collection.update_one(
                {"name": user_name}, {"$set": {"playlists": playlists}}
            )
    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error deleting playlist {playlist_name} from owner {user_name} in database"
        )
        raise BaseUserRepositoryError from exception


async def update_playlist_name(
    old_playlist_name: str, new_playlist_name: str, collection: AsyncIOMotorCollection
) -> None:
    """Update playlist name with a new one

    Args:
        old_playlist_name: old name
        new_playlist_name: new name
        collection: user collection

    Raises:
        BaseUserRepositoryError: updating playlist name
    """
    try:
        # has to be done sequentially, pull and push on the same query generates errors
        await collection.update_many(
            {"saved_playlists": old_playlist_name},
            {"$set": {"saved_playlists.$": new_playlist_name}},
        )
        await collection.update_many(
            {"playlists": old_playlist_name},
            {"$set": {"playlists.$": new_playlist_name}},
        )

    except Exception as exception:
        base_user_repository_logger.exception(
            f"Error updating playlist name {old_playlist_name} "
            f"to {new_playlist_name} in database"
        )
        raise BaseUserRepositoryError from exception


async def get_user_relevant_playlist_names(
    user_name: str, collection: AsyncIOMotorCollection
) -> list[str]:
    """Get user relevant playlist names

    Args:
        user_name: user name
        collection: user collection

    Returns:
        the playlist names of the playlists relevant to the user
    """
    user_data = await collection.find_one(
        {"name": user_name}, {"playlists": 1, "saved_playlists": 1, "_id": 0}
    )

    validate_user_exists(user_data)
    assert user_data

    playlist_names = user_data["playlists"] + user_data["saved_playlists"]

    return playlist_names


async def get_user_playlist_names(
    user_name: str, collection: AsyncIOMotorCollection
) -> list[str]:
    """Get user created playlist names

    Args:
        user_name: user name
        collection: user collection

    Returns:
        the playlist names of the user created playlists
    """
    user_data = await collection.find_one({"name": user_name}, {"playlists": 1, "_id": 0})

    validate_user_exists(user_data)
    assert user_data

    return user_data["playlists"]


async def get_user_playback_history_names(
    user_name: str, collection: AsyncIOMotorCollection
) -> list[str]:
    """Get user playback history song names

    Args:
        user_name: user name
        collection: user collection

    Returns:
        the user playback history
    """
    user_data = await collection.find_one(
        {"name": user_name}, {"playback_history": 1, "_id": 0}
    )

    validate_user_exists(user_data)
    assert user_data

    return user_data["playback_history"]
