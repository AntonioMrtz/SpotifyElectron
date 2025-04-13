"""
Song collections provider
"""

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorGridFSBucket

from app.database.database_schema import DatabaseCollection
from app.database.DatabaseConnectionManager import DatabaseConnectionManager
from app.spotify_electron.song.blob.song_schema import SongDocument


def get_gridfs_song_collection() -> AsyncIOMotorGridFSBucket:
    """Get gridfs collection for managing song files

    Returns:
        AsyncIOMotorGridFSBucket: the GridFS song collection
    """
    return DatabaseConnectionManager.get_gridfs_collection_connection(
        DatabaseCollection.SONG_BLOB_DATA
    )


def get_blob_song_collection() -> AsyncIOMotorCollection[SongDocument]:
    """Get BLOB architecture song collection

    Returns:
        AsyncIOMotorCollection[SongDocument]: song collection
    """
    return DatabaseConnectionManager.get_collection_connection(
        DatabaseCollection.SONG_BLOB_FILE
    )
