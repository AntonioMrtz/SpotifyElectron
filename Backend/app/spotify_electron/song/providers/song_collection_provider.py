"""
Song collections provider based on selected architecture
"""

from motor.motor_asyncio import AsyncIOMotorCollection

from app.common.app_schema import AppArchitecture, AppEnvironment
from app.common.PropertiesManager import PropertiesManager
from app.database.database_schema import DatabaseCollection
from app.database.DatabaseConnectionManager import DatabaseConnectionManager
from app.spotify_electron.song.base_song_schema import BaseSongDocument


def get_song_collection() -> AsyncIOMotorCollection[BaseSongDocument]:
    """Get song collection

    Returns:
        AsyncIOMotorCollection: the song collection depending on architecture
    """
    repository_map: dict[AppArchitecture, AsyncIOMotorCollection] = {
        AppArchitecture.ARCH_BLOB: DatabaseConnectionManager.get_collection_connection(
            DatabaseCollection.SONG_BLOB_FILE
        ),
        AppArchitecture.ARCH_SERVERLESS: DatabaseConnectionManager.get_collection_connection(
            DatabaseCollection.SONG_STREAMING
        ),
    }
    current_architecture = getattr(PropertiesManager, AppEnvironment.ARCHITECTURE_ENV_NAME)
    return repository_map.get(current_architecture, repository_map[AppArchitecture.ARCH_BLOB])
