"""
Song collections provider
"""

from motor.motor_asyncio import AsyncIOMotorCollection

from app.database.database_schema import DatabaseCollection
from app.database.DatabaseConnectionManager import DatabaseConnectionManager
from app.spotify_electron.song.serverless.song_schema import SongDocument


def get_serverless_song_collection() -> AsyncIOMotorCollection[SongDocument]:
    """Get serverless architecture song collection

    Returns:
        AsyncIOMotorCollection[SongDocument]: song collection
    """
    return DatabaseConnectionManager.get_collection_connection(
        DatabaseCollection.SONG_BLOB_FILE
    )
