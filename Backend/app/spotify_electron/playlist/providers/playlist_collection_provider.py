"""
Provider class for supplying playlist collection connection with database
"""

from pymongo.collection import Collection

from app.database.database_connection_provider import DatabaseConnection
from app.database.database_schema import DatabaseCollection


def get_playlist_collection() -> Collection:
    """Get playlist collection

    Returns:
        Collection: the playlist collection
    """
    return DatabaseConnection.connection_instance.get_collection_connection(
        DatabaseCollection.PLAYLIST
    )
