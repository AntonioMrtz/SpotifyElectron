from app.boostrap.PropertiesManager import PropertiesManager
from app.constants.set_up_constants import MONGO_URI_ENV_NAME
from app.exceptions.exceptions_schema import SpotifyElectronException
from app.logging.logger_constants import LOGGING_DATABASE
from app.logging.logging_schema import SpotifyElectronLogger
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

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
            except DatabasePingFailed:
                raise
            except Exception as error:
                database_logger.critical(
                    f"Error establishing connection with database: {error}"
                )
            else:
                database_logger.info(
                    "Connection established successfully with database"
                )

    def _ping_database_connection(self) -> bool:
        """Pings database connection

        Raises:
            DatabasePingFailed: if ping failed

        Returns:
            bool: if ping was successful
        """
        if self.connection is not None:
            ping_result = self.connection.command("ping")
            if not ping_result:
                raise DatabasePingFailed()
        return True


class DatabasePingFailed(SpotifyElectronException):
    def __init__(self):
        super().__init__("DatabasePingFailed")
