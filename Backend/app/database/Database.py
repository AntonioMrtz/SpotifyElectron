import sys
from enum import StrEnum
from typing import Any

from gridfs import GridFS
from pymongo.errors import ConnectionFailure
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from app.common.PropertiesManager import PropertiesManager
from app.common.set_up_constants import MONGO_URI_ENV_NAME
from app.exceptions.exceptions_schema import SpotifyElectronException
from app.logging.logging_constants import LOGGING_DATABASE
from app.logging.logging_schema import SpotifyElectronLogger

database_logger = SpotifyElectronLogger(LOGGING_DATABASE).getLogger()


class DatabaseCollections(StrEnum):
    """A class to store the existing name of the collections in the database"""

    USER = "users"
    ARTIST = "artists"
    PLAYLIST = "playlists"
    SONG_STREAMING = "songs.streaming"
    SONG_BLOB_FILE = "songs.files"
    SONG_BLOB_DATA = "songs"


class DatabaseMeta(type):
    """The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=DatabaseMeta):
    """Singleton instance of the MongoDb connection"""

    TESTING_COLLECTION_NAME_PREFIX = "test."

    def __init__(self):
        if not hasattr(self, "connection"):
            try:
                uri = getattr(PropertiesManager, MONGO_URI_ENV_NAME)
                self.collection_name_prefix = self._get_collection_name_prefix()
                self.connection = MongoClient(uri, server_api=ServerApi("1"))[
                    "SpotifyElectron"
                ]
                self._ping_database_connection()
            except DatabasePingFailed as error:
                self._handle_database_connection_error(error)
            except UnexpectedDatabasePingFailed as error:
                self._handle_database_connection_error(error)
            except Exception as error:
                self._handle_database_connection_error(error)

    def _ping_database_connection(self):
        """Pings database connection"""
        try:
            ping_result = self.connection.command("ping")
            self._check_ping_result(ping_result)
        except ConnectionFailure as exception:
            raise DatabasePingFailed from exception
        except Exception as exception:
            raise UnexpectedDatabasePingFailed from exception

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

    def get_collection_connection(self, collection_name: DatabaseCollections) -> Any:
        """Returns the connection with a collection

        Args:
            collection_name (str): the collection name

        Returns:
            Any: the connection to the collection
        """
        return Database().connection[self.collection_name_prefix + collection_name]

    def get_gridfs_collection_connection(
        self, collection_name: DatabaseCollections
    ) -> Any:
        """Returns the connection with gridfs collection

        Args:
            collection_name (DatabaseCollections): the collection name

        Returns:
            Any: the gridfs collection connection
        """
        return GridFS(
            Database.get_instance().connection,
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
