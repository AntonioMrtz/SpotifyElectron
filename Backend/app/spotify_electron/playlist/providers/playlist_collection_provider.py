"""
Provider class for supplying playlist collection connection with database
"""

from pymongo.collection import Collection

from app.database.database_schema import DatabaseCollection
from app.database.DatabaseConnectionManager import DatabaseConnectionManager


def get_playlist_collection() -> Collection:
    """Get playlist collection

    Returns:
        Collection: the playlist collection
    """
    return DatabaseConnectionManager.get_collection_connection(DatabaseCollection.PLAYLIST)
