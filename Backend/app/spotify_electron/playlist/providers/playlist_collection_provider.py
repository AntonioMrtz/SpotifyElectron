"""
Provider class for supplying playlist collection connection with database
"""

from motor.motor_asyncio import AsyncIOMotorCollection

from app.database.database_schema import DatabaseAsyncIOMotorCollection
from app.database.DatabaseConnectionManager import DatabaseConnectionManager


def get_playlist_collection() -> AsyncIOMotorCollection:
    """Get playlist collection

    Returns:
        AsyncIOMotorCollection: the playlist collection
    """
    return DatabaseConnectionManager.get_collection_connection(
        DatabaseAsyncIOMotorCollection.PLAYLIST
    )
