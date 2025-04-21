"""Database connection provider"""

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorGridFSBucket

from app.common.app_schema import AppEnvironmentMode
from app.database.database_schema import (
    BaseDatabaseConnection,
    DatabaseCollection,
    DatabasePingFailedError,
)
from app.database.DatabaseProductionConnection import DatabaseProductionConnection
from app.database.DatabaseTestingConnection import DatabaseTestingConnection


class DatabaseConnectionManager:
    """Manages the unique database connection and exposes it to the app"""

    __connection: type[BaseDatabaseConnection]
    """Connection instance of database"""
    __connection_mapping: dict[AppEnvironmentMode, type[BaseDatabaseConnection]] = {
        AppEnvironmentMode.PROD: DatabaseProductionConnection,
        AppEnvironmentMode.DEV: DatabaseProductionConnection,
        AppEnvironmentMode.TEST: DatabaseTestingConnection,
    }
    """Mapping between environment mode and database connection"""

    @classmethod
    def get_collection_connection(
        cls, collection_name: DatabaseCollection
    ) -> AsyncIOMotorCollection:
        """Get a connection to a collection

        Args:
            collection_name: collection name

        Returns:
            the connection to the selected collection
        """
        cls.__assert_connection_is_initialized()

        return cls.__connection.get_collection_connection(collection_name)

    @classmethod
    async def init_database_connection(
        cls, environment: AppEnvironmentMode, connection_uri: str
    ) -> None:
        """Initializes the database connection and loads its unique instance\
            based on current environment value

        Args:
            environment: the current environment value
            connection_uri: the database connection uri
    """
        database_connection_class = cls.__connection_mapping.get(
            environment, DatabaseProductionConnection
        )
        await database_connection_class.init_connection(connection_uri)
        cls.__connection = database_connection_class

    @classmethod
    def check_database_health(cls) -> bool:
        """
        Check if the database connection is established and working.
        This method attempts to verify that the connection to the database
        is active and functioning properly.

        Raises:
            DatabasePingFailedError: When the ping command fails or an error occurs while
            communicating with the database

        Returns:
            bool: True if the database connection is working, False otherwise.
        """
        try:
            if cls.connection is None:
                cls._logger.error("Database connection not initialized")
                return False
            if cls.connection.check_connection_health():
                cls._logger.info("Connected to database cluster")
                return True
            else:
                cls._logger.error("Database connection failed")
                return False
        except DatabasePingFailedError as exception:
            cls._logger.exception("Database ping command failed")
            raise DatabasePingFailedError from exception

    @classmethod
    def close_database_connection(cls) -> None:
        """Close database connection"""
        cls.__assert_connection_is_initialized()

        cls.__connection.close_connection()

    @classmethod
    def get_gridfs_collection_connection(
        cls,
        collection_name: DatabaseCollection,
    ) -> AsyncIOMotorGridFSBucket:
        """Get GridFS collection

        Args:
            collection_name: collection name

        Returns:
            the GridFS collection
        """
        cls.__assert_connection_is_initialized()
        return cls.__connection.get_gridfs_collection_connection(collection_name)

    @classmethod
    def __assert_connection_is_initialized(
        cls,
    ):
        assert cls.__connection is not None, (
            "DatabaseConnectionManager connection is not initialized"
        )
