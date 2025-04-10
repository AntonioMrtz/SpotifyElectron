"""In-memory Database connection for testing"""

from app.database.database_schema import BaseDatabaseConnection


class DatabaseTestingConnection(BaseDatabaseConnection):
    """Database connection for testing. Uses an in-memory database"""

    TESTING_COLLECTION_NAME_PREFIX = "test."

    @classmethod
    def _get_mongo_client(cls):
        from mongomock.gridfs import enable_gridfs_integration
        from mongomock_motor import AsyncMongoMockClient

        """Get mock Mongo client class

        Returns:
            AsyncMongoMockClient: the mock Mongo client class
        """
        enable_gridfs_integration()
        return AsyncMongoMockClient

    @classmethod
    def _get_collection_name_prefix(cls) -> str:
        """Returns prefix for testing

        Returns:
            str: the testing prefix for collections
        """
        return cls.TESTING_COLLECTION_NAME_PREFIX
