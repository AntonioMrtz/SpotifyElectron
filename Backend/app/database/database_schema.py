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
from pymongo.errors import PyMongoError
from pymongo.server_api import ServerApi

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

    __DATABASE_NAME = "SpotifyElectron"
    """Database name"""
    _connection: AsyncIOMotorDatabase
    """Database connection"""
    _client: AsyncIOMotorClient
    """Database client"""
    __collection_name_prefix: str = ""
    """Database collection prefix applied to all collections"""
    _logger = SpotifyElectronLogger(LOGGING_DATABASE_CONNECTION).get_logger()

    @classmethod
    async def init_connection(cls, uri: str):
        """Init database connection

        Args:
            uri: database connection URI
        """
        try:
            cls.__collection_name_prefix = cls._get_collection_name_prefix()
            cls._client = cls._get_mongo_client()(uri, server_api=ServerApi("1"))
            # Needed because of https://github.com/encode/starlette/issues/1315#issuecomment-980784457
            cls._client.get_io_loop = get_event_loop
            await cls._client.admin.command("ping")
            cls._connection = cls._client[cls.__DATABASE_NAME]
        except Exception as exception:
            cls._logger.critical(f"Error establishing connection with database: {exception}")
            sys.exit("Database connection failed. Stopping server")

    @classmethod
    def close_connection(cls) -> None:
        """Close client connection. If the instance is used again the connection
        will be automatically re-opened.
        On version >=4.0 connection won't be accesible after closing
        https://motor.readthedocs.io/en/stable/api-tornado/motor_client.html#motor.motor_tornado.MotorClient.close
        """
        cls.__assert_connection_is_initialized()
        cls._client.close()

    @classmethod
    @abstractmethod
    def _get_mongo_client(cls) -> type[AsyncIOMotorClient]:
        """Get mongo client class

        Returns:
            the mongo client class
        """
        pass

    @classmethod
    @abstractmethod
    def _get_collection_name_prefix(cls) -> str:
        """Returns collection prefix

        Returns:
            the prefix for collections
        """
        pass

    @classmethod
    def get_collection_connection(
        cls, collection_name: DatabaseCollection
    ) -> AsyncIOMotorCollection:
        """Returns the connection with a collection

        Args:
            collection_name: the collection name

        Returns:
            the connection to the collection
        """
        cls.__assert_connection_is_initialized()
        return cls._connection[cls.__collection_name_prefix + collection_name]

    @classmethod
    def get_gridfs_collection_connection(
        cls, collection_name: DatabaseCollection
    ) -> AsyncIOMotorGridFSBucket:
        """Returns the connection with gridfs collection

        Args:
            collection_name: the collection name

        Returns:
            the gridfs collection connection
        """
        cls.__assert_connection_is_initialized()
        return AsyncIOMotorGridFSBucket(
            cls._connection,
            bucket_name=cls.__collection_name_prefix + collection_name,
        )

    @classmethod
    def __assert_connection_is_initialized(
        cls,
    ):
        assert cls._connection is not None, "Database connection is not initialized"

    @classmethod
    async def check_connection_health(cls) -> bool | None:
        """Check the health status of the database connection.

        Raises:
            DatabasePingFailedError: When the ping command fails or an error occurs while
            communicating with the database

        Returns:
            bool: True if the database connection is healthy, False otherwise
        """
        try:
            ping_response = await cls._client.admin.command("ping")
            cls._logger.info("Database connection health check successful")
            if isinstance(ping_response, dict) and "ok" in ping_response:
                cls._logger.debug(f"Ping response: {ping_response}")
                return int(ping_response.get("ok", 0)) == 1
        except PyMongoError as exception:
            cls._logger.exception("Database ping command failed")
            raise DatabasePingFailedError from exception


class DatabasePingFailedError(SpotifyElectronError):
    """Database ping failure"""

    ERROR = "Database ping failed"

    def __init__(self):
        super().__init__(self.ERROR)
