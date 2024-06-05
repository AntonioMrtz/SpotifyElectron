from gridfs import GridFS
from pymongo.collection import Collection

from app.common.PropertiesManager import PropertiesManager
from app.common.set_up_constants import (
    ARCH_BLOB,
    ARCH_STREAMING_SERVERLESS_FUNCTION,
    ARCHITECTURE_ENV_NAME,
)
from app.database.Database import Database, DatabaseCollection


def get_song_collection() -> Collection:
    """Get song collection

    Returns:
        Collection: the song collection depending on architecture
    """
    repository_map = {
        ARCH_BLOB: Database().get_collection_connection(
            DatabaseCollection.SONG_BLOB_FILE
        ),
        ARCH_STREAMING_SERVERLESS_FUNCTION: Database().get_collection_connection(
            DatabaseCollection.SONG_STREAMING
        ),
    }
    return repository_map.get(PropertiesManager.__getattribute__(ARCHITECTURE_ENV_NAME))  # type: ignore


def get_gridfs_song_collection() -> GridFS:
    """Get gridfs collection for managing song files

    :return GridFS: the gridfs song collection
    """
    return Database().get_gridfs_collection_connection(
        DatabaseCollection.SONG_BLOB_DATA
    )
