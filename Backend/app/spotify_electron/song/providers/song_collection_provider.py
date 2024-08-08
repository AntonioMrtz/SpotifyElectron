"""
Provider class for supplying song collection connection with database depending on the\
      architecture on song selected
"""

from gridfs import GridFS
from pymongo.collection import Collection

from app.common.app_schema import AppArchitecture, AppEnviroment
from app.common.PropertiesManager import PropertiesManager
from app.database.database_connection_provider import DatabaseConnection
from app.database.database_schema import DatabaseCollection


def get_song_collection() -> Collection:
    """Get song collection

    Returns:
        Collection: the song collection depending on architecture
    """
    repository_map = {
        AppArchitecture.ARCH_BLOB: DatabaseConnection.connection_instance.get_collection_connection(  # noqa: E501
            DatabaseCollection.SONG_BLOB_FILE
        ),
        AppArchitecture.ARCH_STREAMING_SERVERLESS_FUNCTION: DatabaseConnection.connection_instance.get_collection_connection(  # noqa: E501
            DatabaseCollection.SONG_STREAMING
        ),
    }
    return repository_map.get(
        PropertiesManager.__getattribute__(AppEnviroment.ARCHITECTURE_ENV_NAME)
    )  # type: ignore


def get_gridfs_song_collection() -> GridFS:
    """Get gridfs collection for managing song files

    :return GridFS: the gridfs song collection
    """
    return DatabaseConnection.connection_instance.get_gridfs_collection_connection(
        DatabaseCollection.SONG_BLOB_DATA
    )
