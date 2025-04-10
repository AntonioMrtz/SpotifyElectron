"""Database connection for production"""

from pymongo import MongoClient

from app.database.database_schema import BaseDatabaseConnection


class DatabaseProductionConnection(BaseDatabaseConnection):
    """Database connection for production"""

    @classmethod
    def _get_mongo_client(cls) -> type[MongoClient]:
        """Get Mongo client class

        Returns:
            type[MongoClient]: the Mongo client class
        """
        return MongoClient

    @classmethod
    def _get_collection_name_prefix(cls) -> str:
        """Returns prod prefix for collections

        Returns:
            str: the prod prefix for collections
        """
        return ""
