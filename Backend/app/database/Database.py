from pymongo.errors import ConnectionFailure
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from app.boostrap.PropertiesManager import PropertiesManager
from app.constants.set_up_constants import MONGO_URI_ENV_NAME
from app.exceptions.exceptions_schema import SpotifyElectronException
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
            if not ping_result:
                raise DatabasePingFailed()
        except ConnectionFailure:
            raise DatabasePingFailed()
        except Exception as error:
            raise UnexpectedDatabasePingFailed(error)

    def _handle_database_connection_error(self, error: Exception) -> None:
        """Handles database connection errors"""
        database_logger.critical(
            f"Error establishing connection with database: {error}"
        )

    @staticmethod
    def get_instance():
        """Method to retrieve the singleton instance"""
        return Database()


class DatabasePingFailed(SpotifyElectronException):
    """Exception for database ping failure"""

    DATABASE_PING_FAILED = "Ping to the database failed"

    def __init__(self):
        super().__init__(self.DATABASE_PING_FAILED)


class UnexpectedDatabasePingFailed(SpotifyElectronException):
    """Exception for unexpected database ping failure"""

    UNEXPECTED_DATABASE_PING_FAILED = "Unexpected error while pinging to the database"

    def __init__(self, exception: Exception):
        super().__init__(f"{self.UNEXPECTED_DATABASE_PING_FAILED} : {exception}")
