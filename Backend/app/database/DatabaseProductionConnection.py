"""Database connection for production"""

from motor.motor_asyncio import AsyncIOMotorClient

from app.database.database_schema import BaseDatabaseConnection


class DatabaseProductionConnection(BaseDatabaseConnection):
    """Database connection for production"""

    @classmethod
    def _get_mongo_client(cls) -> type[AsyncIOMotorClient]:
        """Get Mongo client class

        Returns:
            the Mongo client class
        """
        return AsyncIOMotorClient

    @classmethod
    def _get_collection_name_prefix(cls) -> str:
        """Returns prod prefix for collections

        Returns:
            the prod prefix for collections
        """
        return ""
