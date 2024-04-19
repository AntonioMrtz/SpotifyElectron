from pymongo.errors import ConnectionFailure
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from app.common.PropertiesManager import PropertiesManager
from app.constants.set_up_constants import MONGO_URI_ENV_NAME
from app.database.database_exceptions import (
    DatabasePingFailed,
    UnexpectedDatabasePingFailed,
)
from app.logging.logger_constants import LOGGING_DATABASE
from app.logging.logging_schema import SpotifyElectronLogger

database_logger = SpotifyElectronLogger(LOGGING_DATABASE).getLogger()


class DatabaseMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=DatabaseMeta):
    """Singleton instance of the MongoDb connection"""

    connection = None

    def __init__(self):
        if self.connection is None:
            try:
                uri = getattr(PropertiesManager, MONGO_URI_ENV_NAME)
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
        if self.connection is None:
            return
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
            ping_result (dict): ping result response

        Raises:
            DatabasePingFailed: if ping result is not OK
        """
        if not ping_result:
            raise DatabasePingFailed

    def _handle_database_connection_error(self, error: Exception) -> None:
        """Handles database connection errors"""
        database_logger.critical(
            f"Error establishing connection with database: {error}"
        )

    @staticmethod
    def get_instance():
        """Method to retrieve the singleton instance"""
        return Database()
