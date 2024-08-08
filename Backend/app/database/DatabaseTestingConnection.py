"""In-memory Database connection for testing"""

from mongomock.gridfs import enable_gridfs_integration
from mongomock.mongo_client import MongoClient as MongoClientMock

from app.database.database_schema import BaseDatabaseConnection


class DatabaseTestingConnection(BaseDatabaseConnection):
    """Database connection for testing. Uses an in-memory database"""

    TESTING_COLLECTION_NAME_PREFIX = "test."

    def _get_mongo_client(self):
        """Get mock Mongo client class

        Returns:
            Any: the mock Mongo client class
        """
        enable_gridfs_integration()
        return MongoClientMock

    def _get_collection_name_prefix(self) -> str:
        """Returns prefix for testing

        Returns:
            str: the testing prefix for collections
        """
        return self.TESTING_COLLECTION_NAME_PREFIX
