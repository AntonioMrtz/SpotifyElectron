"""Database connection provider"""

from motor.motor_asyncio import AsyncIOMotorCollection

from app.common.app_schema import AppEnvironmentMode
from app.database.database_schema import BaseDatabaseConnection, DatabaseAsyncIOMotorCollection
from app.database.DatabaseProductionConnection import DatabaseProductionConnection
from app.database.DatabaseTestingConnection import DatabaseTestingConnection
from app.logging.logging_constants import LOGGING_DATABASE_MANAGER
from app.logging.logging_schema import SpotifyElectronLogger


class DatabaseConnectionManager:
    """Manages the unique database connection and exposes it to the app"""

    connection: type[BaseDatabaseConnection]
    """Connection instance of database"""
    database_connection_mapping: dict[AppEnvironmentMode, type[BaseDatabaseConnection]] = {
        AppEnvironmentMode.PROD: DatabaseProductionConnection,
        AppEnvironmentMode.DEV: DatabaseProductionConnection,
        AppEnvironmentMode.TEST: DatabaseTestingConnection,
    }
    """Mapping between environment mode and database connection"""
    _logger = SpotifyElectronLogger(LOGGING_DATABASE_MANAGER).get_logger()

    @classmethod
    def get_collection_connection(
        cls, collection_name: DatabaseAsyncIOMotorCollection
    ) -> AsyncIOMotorCollection:
        """Get a connection to a collection

        Args:
            collection_name (DatabaseAsyncIOMotorCollection): collection name

        Returns:
            AsyncIOMotorCollection: the connection to the selected collection
        """
        assert cls.connection is not None, "DatabaseConnectionManager connection is not init"

        return cls.connection.get_collection_connection(collection_name)

    @classmethod
    async def init_database_connection(
        cls, environment: AppEnvironmentMode, connection_uri: str
    ) -> None:
        """Initializes the database connection and loads its unique instance\
            based on current environment value

        Args:
            environment (AppEnvironmentMode): the current environment value
            connection_uri (str): the database connection uri
        """
        database_connection_class = cls.database_connection_mapping.get(
            environment, DatabaseProductionConnection
        )
        await database_connection_class.init_connection(connection_uri)
        cls.connection = database_connection_class
