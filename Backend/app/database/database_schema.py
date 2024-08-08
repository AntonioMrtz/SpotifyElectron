"""Database schema for domain model"""

import sys
from abc import abstractmethod
from enum import StrEnum
from functools import wraps
from typing import Any

from gridfs import GridFS
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure
from pymongo.server_api import ServerApi

from app.common.app_schema import AppEnviroment
from app.common.PropertiesManager import PropertiesManager
from app.exceptions.base_exceptions_schema import SpotifyElectronException
from app.logging.logging_constants import LOGGING_DATABASE
from app.logging.logging_schema import SpotifyElectronLogger


class DatabaseCollection(StrEnum):
    """Collection names present in database"""

    USER = "users"
    ARTIST = "artists"
    PLAYLIST = "playlists"
    SONG_STREAMING = "songs.streaming"
    SONG_BLOB_FILE = "songs.files"
    SONG_BLOB_DATA = "songs"


def __is_connection__init__(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if BaseDatabaseConnection.connection is not None:
            return func(*args, **kwargs)

    return wrapper


class BaseDatabaseConnection:
    """MongoDB connection Instance"""

    DATABASE_NAME = "SpotifyElectron"
    connection = None
    collection_name_prefix = None

    def __init__(self):
        self._logger = SpotifyElectronLogger(LOGGING_DATABASE).getLogger()
        try:
            uri = getattr(PropertiesManager, AppEnviroment.MONGO_URI_ENV_NAME)
            BaseDatabaseConnection.collection_name_prefix = self._get_collection_name_prefix()
            client = self._get_mongo_client()
            BaseDatabaseConnection.connection = client(uri, server_api=ServerApi("1"))[
                self.DATABASE_NAME
            ]
            self._ping_database_connection()
        except (
            DatabasePingFailed,
            UnexpectedDatabasePingFailed,
            Exception,
        ) as exception:
            self._handle_database_connection_error(exception)

    @__is_connection__init__
    def _ping_database_connection(self):
        """Pings database connection"""
        try:
            ping_result = BaseDatabaseConnection.connection.command("ping")  # type: ignore
            self._check_ping_result(ping_result)
        except ConnectionFailure as exception:
            raise DatabasePingFailed from exception
        except Exception as exception:
            raise UnexpectedDatabasePingFailed from exception

    @abstractmethod
    def _get_mongo_client(self) -> Any:
        """Get mongo client

        Returns:
            Any: the mongo client
        """
        pass

    @abstractmethod
    def _get_collection_name_prefix(self) -> str:
        """Returns collection prefix

        Returns:
            str: the prefix for collections
        """
        pass

    @__is_connection__init__
    @staticmethod
    def get_collection_connection(collection_name: DatabaseCollection) -> Collection:
        """Returns the connection with a collection

        Args:
            collection_name (str): the collection name

        Returns:
            Any: the connection to the collection
        """
        return BaseDatabaseConnection.connection[  # type: ignore
            BaseDatabaseConnection.collection_name_prefix + collection_name  # type: ignore
        ]

    @__is_connection__init__
    @staticmethod
    def get_gridfs_collection_connection(collection_name: DatabaseCollection) -> Any:
        """Returns the connection with gridfs collection

        Args:
            collection_name (DatabaseCollections): the collection name

        Returns:
            Any: the gridfs collection connection
        """
        return GridFS(
            BaseDatabaseConnection.connection,  # type: ignore
            collection=BaseDatabaseConnection.collection_name_prefix + collection_name,  # type: ignore
        )

    def _handle_database_connection_error(self, error: Exception) -> None:
        """Handles database connection errors"""
        self._logger.critical(f"Error establishing connection with database: {error}")
        sys.exit("Database connection failed, stopping server")

    def _check_ping_result(self, ping_result: dict[str, Any]):
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
