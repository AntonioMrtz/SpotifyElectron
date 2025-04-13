"""
Playlist collections provider
"""

from motor.motor_asyncio import AsyncIOMotorCollection

from app.database.database_schema import DatabaseCollection
from app.database.DatabaseConnectionManager import DatabaseConnectionManager
from app.spotify_electron.playlist.playlist_schema import PlaylistDocument


def get_playlist_collection() -> AsyncIOMotorCollection[PlaylistDocument]:
    """Get playlist collection

    Returns:
        AsyncIOMotorCollection: the playlist collection
    """
    return DatabaseConnectionManager.get_collection_connection(DatabaseCollection.PLAYLIST)
