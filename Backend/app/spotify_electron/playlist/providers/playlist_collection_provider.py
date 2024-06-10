"""
Provider class for supplying playlist collection connection with database
"""

from pymongo.collection import Collection

from app.database.Database import Database, DatabaseCollection


def get_playlist_collection() -> Collection:
    """Get playlist collection

    Returns:
        Collection: the playlist collection
    """
    return Database().get_collection_connection(DatabaseCollection.PLAYLIST)
