"""Database connection for production"""

from typing import Any

from mongomock import MongoClient

from app.database.database_schema import BaseDatabaseConnection


class DatabaseProductionConnection(BaseDatabaseConnection):
    """Database connection for production"""

    def _get_mongo_client(self) -> Any:
        """Get Mongo client class

        Returns:
            Any: the Mongo client class
        """
        return MongoClient

    def _get_collection_name_prefix(self) -> str:
        """Returns prod prefix for collections

        Returns:
            str: the prod prefix for collections
        """
        return ""
