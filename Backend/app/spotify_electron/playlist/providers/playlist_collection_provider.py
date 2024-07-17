"""
Provider class for supplying playlist collection connection with database
"""

from pymongo.collection import Collection

from app.database.DatabaseConnection import DatabaseCollection, DatabaseConnection


def get_playlist_collection() -> Collection:
    """Get playlist collection

    Returns:
        Collection: the playlist collection
    """
    return DatabaseConnection.get_collection_connection(DatabaseCollection.PLAYLIST)
