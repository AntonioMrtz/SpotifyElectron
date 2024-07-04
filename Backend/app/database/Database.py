"""
Manages the unique database connection across the app and provides the modules with the collections\
    needed for persist data.
"""

import sys
from enum import StrEnum
from typing import Any

from gridfs import GridFS
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from app.common.PropertiesManager import PropertiesManager
from app.common.set_up_constants import MONGO_URI_ENV_NAME
from app.exceptions.base_exceptions_schema import SpotifyElectronException
from app.logging.logging_constants import LOGGING_DATABASE
from app.logging.logging_schema import SpotifyElectronLogger
from app.patterns.Singleton import Singleton

database_logger = SpotifyElectronLogger(LOGGING_DATABASE).getLogger()


class DatabaseCollection(StrEnum):
    """Collection names present in database"""

    USER = "users"
    ARTIST = "artists"
    PLAYLIST = "playlists"
    SONG_STREAMING = "songs.streaming"
    SONG_BLOB_FILE = "songs.files"
    SONG_BLOB_DATA = "songs"


class Database(metaclass=Singleton):
    """Singleton instance of the MongoDb connection"""

    TESTING_COLLECTION_NAME_PREFIX = "test."
    DATABASE_NAME = "SpotifyElectron"

    def __init__(self):
        if not hasattr(self, "connection"):
            try:
                uri = getattr(PropertiesManager, MONGO_URI_ENV_NAME)
                self.collection_name_prefix = self._get_collection_name_prefix()
                client = self._get_mongo_client_class()
                self.connection = client(uri, server_api=ServerApi("1"))[
                    self.DATABASE_NAME
                ]
                self._ping_database_connection()
            except (
                DatabasePingFailed,
                UnexpectedDatabasePingFailed,
                Exception,
            ) as exception:
                self._handle_database_connection_error(exception)

    def _ping_database_connection(self):
        """Pings database connection"""
        try:
            ping_result = self.connection.command("ping")
            self._check_ping_result(ping_result)
        except ConnectionFailure as exception:
            raise DatabasePingFailed from exception
        except Exception as exception:
            raise UnexpectedDatabasePingFailed from exception

    def _get_mongo_client_class(self):
        """Get Mongo client class

        Returns:
            _type_: the Mongo client class
        """
        if PropertiesManager.is_testing_enviroment():
            from mongomock.gridfs import enable_gridfs_integration
            from mongomock.mongo_client import MongoClient as MongoClientMock

            enable_gridfs_integration()
            return MongoClientMock

        return MongoClient

    def _check_ping_result(self, ping_result: dict):
        """Checks if ping result is OK

        Args:
        ----
            ping_result (dict): ping result response

        Raises:
        ------
            DatabasePingFailed: if ping result is not OK

        """
        if not ping_result:
            raise DatabasePingFailed

    def _handle_database_connection_error(self, error: Exception) -> None:
        """Handles database connection errors"""
        database_logger.critical(
            f"Error establishing connection with database: {error}"
        )
        sys.exit("Database connection failed, stopping server")

    def _get_collection_name_prefix(self) -> str:
        """Returns prefix for testing if test enviroment

        Returns:
            str: the testing prefix for collections
        """
        return (
            self.TESTING_COLLECTION_NAME_PREFIX
            if PropertiesManager.is_testing_enviroment()
            else ""
        )

    @staticmethod
    def get_instance():
        """Method to retrieve the singleton instance"""
        return Database()

    def get_collection_connection(
        self, collection_name: DatabaseCollection
    ) -> Collection:
        """Returns the connection with a collection

        Args:
            collection_name (str): the collection name

        Returns:
            Any: the connection to the collection
        """
        return Database().connection[self.collection_name_prefix + collection_name]  # type: ignore

    def get_gridfs_collection_connection(
        self, collection_name: DatabaseCollection
    ) -> Any:
        """Returns the connection with gridfs collection

        Args:
            collection_name (DatabaseCollections): the collection name

        Returns:
            Any: the gridfs collection connection
        """
        return GridFS(
            Database.get_instance().connection,  # type: ignore
            collection=self.collection_name_prefix + collection_name,
        )


class DatabasePingFailed(SpotifyElectronException):
    """Exception for database ping failure"""

    ERROR = "Ping to the database failed"

    def __init__(self):
        super().__init__(self.ERROR)


class UnexpectedDatabasePingFailed(SpotifyElectronException):
    """Exception for unexpected database ping failure"""

    ERROR = "Unexpected error while pinging to the database"

    def __init__(self):
        super().__init__(self.ERROR)
