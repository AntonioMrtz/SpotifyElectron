"""Database schema for domain model"""

import sys
from abc import abstractmethod
from enum import StrEnum

from gridfs import GridFS
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from app.common.app_schema import AppEnvironment
from app.common.PropertiesManager import PropertiesManager
from app.exceptions.base_exceptions_schema import SpotifyElectronError
from app.logging.logging_constants import LOGGING_DATABASE_CONNECTION
from app.logging.logging_schema import SpotifyElectronLogger


class DatabaseCollection(StrEnum):
    """Collection names present in database"""

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
    connection: Database
    """Database connection"""
    collection_name_prefix: str = ""
    """Database collection prefix applied to all collections"""
    _logger = SpotifyElectronLogger(LOGGING_DATABASE_CONNECTION).get_logger()

    @classmethod
    def init_connection(cls, uri: str):
        """Init database connection

        Args:
            uri (str): database connection URI
        """
        try:
            uri = getattr(PropertiesManager, AppEnvironment.MONGO_URI_ENV_NAME)
            cls.collection_name_prefix = cls._get_collection_name_prefix()
            client = cls._get_mongo_client()(uri, server_api=ServerApi("1"))
            client.admin.command("ping")
            cls.connection = client[cls.DATABASE_NAME]
        except Exception as exception:
            cls._logger.critical(f"Error establishing connection with database: {exception}")
            sys.exit("Database connection failed, stopping server")

    @classmethod
    @abstractmethod
    def _get_mongo_client(cls) -> type[MongoClient]:
        """Get mongo client class

        Returns:
            type[MongoClient]: the mongo client class
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
    def get_collection_connection(cls, collection_name: DatabaseCollection) -> Collection:
        """Returns the connection with a collection

        Args:
            collection_name (str): the collection name

        Returns:
            Collection: the connection to the collection
        """
        return cls.connection[cls.collection_name_prefix + collection_name]

    @classmethod
    def get_gridfs_collection_connection(cls, collection_name: DatabaseCollection) -> GridFS:
        """Returns the connection with gridfs collection

        Args:
            collection_name (DatabaseCollections): the collection name

        Returns:
            GridFS: the gridfs collection connection
        """
        assert cls.connection is not None, "DatabaseConnectionManager connection is not init"

        return GridFS(
            cls.connection,
            collection=cls.collection_name_prefix + collection_name,
        )


class DatabasePingFailedError(SpotifyElectronError):
    """Database ping failure"""

    ERROR = "Database ping failed"

    def __init__(self):
        super().__init__(self.ERROR)
