"""
Provider class for supplying song collection connection with database depending on the\
      architecture on song selected
"""

from gridfs import GridFS
from pymongo.collection import Collection

from app.common.app_schema import AppArchitecture, AppEnvironment
from app.common.PropertiesManager import PropertiesManager
from app.database.database_schema import DatabaseCollection
from app.database.DatabaseConnectionManager import DatabaseConnectionManager


def get_song_collection() -> Collection:
    """Get song collection

    Returns:
        Collection: the song collection depending on architecture
    """
    repository_map = {
        AppArchitecture.ARCH_BLOB: DatabaseConnectionManager.get_collection_connection(
            DatabaseCollection.SONG_BLOB_FILE
        ),
        AppArchitecture.ARCH_STREAMING_SERVERLESS_FUNCTION: DatabaseConnectionManager.get_collection_connection(  # noqa: E501
            DatabaseCollection.SONG_STREAMING
        ),
    }
    current_architecture = PropertiesManager.__getattribute__(
        AppEnvironment.ARCHITECTURE_ENV_NAME
    )
    return repository_map.get(current_architecture, repository_map[AppArchitecture.ARCH_BLOB])


def get_gridfs_song_collection() -> GridFS:
    """Get gridfs collection for managing song files

    Returns:
        GridFS: the gridfs song collection
    """
    return DatabaseConnectionManager.connection.get_gridfs_collection_connection(
        DatabaseCollection.SONG_BLOB_DATA
    )
