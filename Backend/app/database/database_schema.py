"""Database schema for domain model"""

import sys
from abc import abstractmethod
from asyncio import get_event_loop
from enum import StrEnum

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
    AsyncIOMotorGridFSBucket,
)
from pymongo.server_api import ServerApi

from app.common.app_schema import AppEnvironment
from app.common.PropertiesManager import PropertiesManager
from app.exceptions.base_exceptions_schema import SpotifyElectronError
from app.logging.logging_constants import LOGGING_DATABASE_CONNECTION
from app.logging.logging_schema import SpotifyElectronLogger


class DatabaseAsyncIOMotorCollection(StrEnum):
    """AsyncIOMotorCollection names present in database"""

    USER = "users"
    ARTIST = "artists"
    PLAYLIST = "playlists"
    SONG_STREAMING = "songs.streaming"
    SONG_BLOB_FILE = "songs.files"
    SONG_BLOB_DATA = "songs"


class BaseDatabaseConnection:
    """Base MongoDB connection Instance. Manages a single connection for the whole app"""

    DATABASE_NAME = "SpotifyElectron"
    """Database name"""
    connection: AsyncIOMotorDatabase
    """Database connection"""
    collection_name_prefix: str = ""
    """Database collection prefix applied to all collections"""
    _logger = SpotifyElectronLogger(LOGGING_DATABASE_CONNECTION).get_logger()

    @classmethod
    async def init_connection(cls, uri: str):
        """Init database connection

        Args:
            uri (str): database connection URI
        """
        try:
            uri = getattr(PropertiesManager, AppEnvironment.MONGO_URI_ENV_NAME)
            cls.collection_name_prefix = cls._get_collection_name_prefix()
            client = cls._get_mongo_client()(uri, server_api=ServerApi("1"))
            client.get_io_loop = get_event_loop
            await client.admin.command("ping")
            cls.connection = client[cls.DATABASE_NAME]
        except Exception as exception:
            cls._logger.critical(f"Error establishing connection with database: {exception}")
            sys.exit("Database connection failed. Stopping server")

    @classmethod
    @abstractmethod
    def _get_mongo_client(cls) -> type[AsyncIOMotorClient]:
        """Get mongo client class

        Returns:
            type[MotorClient]: the mongo client class
        """
        pass

    @classmethod
    @abstractmethod
    def _get_collection_name_prefix(cls) -> str:
        """Returns collection prefix

        Returns:
            str: the prefix for collections
        """
        pass

    @classmethod
    def get_collection_connection(
        cls, collection_name: DatabaseAsyncIOMotorCollection
    ) -> AsyncIOMotorCollection:
        """Returns the connection with a collection

        Args:
            collection_name (str): the collection name

        Returns:
            AsyncIOMotorCollection: the connection to the collection
        """
        assert cls.connection is not None, "DatabaseConnectionManager connection is not init"

        return cls.connection[cls.collection_name_prefix + collection_name]

    @classmethod
    def get_gridfs_collection_connection(
        cls, collection_name: DatabaseAsyncIOMotorCollection
    ) -> AsyncIOMotorGridFSBucket:
        """Returns the connection with gridfs collection

        Args:
            collection_name (DatabaseAsyncIOMotorCollections): the collection name

        Returns:
            AsyncIOMotorGridFSBucket: the gridfs collection connection
        """
        assert cls.connection is not None, "DatabaseConnectionManager connection is not init"

        return AsyncIOMotorGridFSBucket(
            cls.connection,
            bucket_name=cls.collection_name_prefix + collection_name,
        )


class DatabasePingFailedError(SpotifyElectronError):
    """Database ping failure"""

    ERROR = "Database ping failed"

    def __init__(self):
        super().__init__(self.ERROR)
