"""
Provider class for supplying user collection connection with database depending on the \
    architecture on the associated user type
"""

from pymongo.collection import Collection

import app.spotify_electron.user.base_user_service as base_user_service
from app.database.database_connection_provider import DatabaseConnection
from app.database.database_schema import DatabaseCollection
from app.logging.logging_constants import LOGGING_USER_COLLECTION_PROVIDER
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.user.user.user_schema import UserType

users_collection_provider_logger = SpotifyElectronLogger(
    LOGGING_USER_COLLECTION_PROVIDER
).getLogger()


def get_user_associated_collection(user_name: str) -> Collection:
    """Returns the user collection according to the user role

    Returns:
        Collection: the user collection
    """
    collection_map = {
        UserType.USER: DatabaseConnection.connection_instance.get_collection_connection(
            DatabaseCollection.USER
        ),
        UserType.ARTIST: DatabaseConnection.connection_instance.get_collection_connection(
            DatabaseCollection.ARTIST
        ),
    }

    user_type = base_user_service.get_user_type(user_name)
    if user_type not in collection_map:
        users_collection_provider_logger.warning(
            f"User {user_name} doesn't have a valid user type "
            f"using {UserType.USER} type instead"
        )
        return collection_map[UserType.USER]
    return collection_map[user_type]


def get_artist_collection() -> Collection:
    """Get artist collection

    Returns:
        Collection: the artist collection
    """
    return DatabaseConnection.connection_instance.get_collection_connection(
        DatabaseCollection.ARTIST
    )


def get_user_collection() -> Collection:
    """Get artist collection

    Returns:
        Collection: the artist collection
    """
    return DatabaseConnection.connection_instance.get_collection_connection(
        DatabaseCollection.USER
    )


def get_all_collections() -> list[Collection]:
    """Get all user collections

    Returns:
        list[Collection]: all the users collections
    """
    collection_map = {
        UserType.USER: DatabaseConnection.connection_instance.get_collection_connection(
            DatabaseCollection.USER
        ),
        UserType.ARTIST: DatabaseConnection.connection_instance.get_collection_connection(
            DatabaseCollection.ARTIST
        ),
    }
    return list(collection_map.values())
