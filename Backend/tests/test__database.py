import os
from unittest.mock import MagicMock, Mock, patch

from app.constants.set_up_constants import MONGO_URI_ENV_NAME
from app.database.Database import (
    Database,
    DatabaseMeta,
    DatabasePingFailed,
    UnexpectedDatabasePingFailed,
)
from pymongo.errors import ConnectionFailure
from pytest import raises


@patch("app.database.Database.MongoClient")
def test_raise_exception_connection_failure(MongoClient, clean_modified_environments):
    def raise_exception_connection_failure(*arg):
        raise ConnectionFailure("ConnectionFailure Simulated exception")

    mock_mongo_client = Mock()

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_mongo_client
    mock_mongo_client.command.side_effect = raise_exception_connection_failure
    MongoClient.return_value = mock_db

    os.environ[MONGO_URI_ENV_NAME] = "mongo_uri"
    DatabaseMeta._instances.clear()
    with raises(DatabasePingFailed):
        Database()._ping_database_connection()


@patch("app.database.Database.MongoClient")
def test_raise_exception_unexpected_connection_failure(
    MongoClient, clean_modified_environments
):
    def raise_exception_connection_failure(*arg):
        raise UnexpectedDatabasePingFailed(Exception())

    mock_mongo_client = Mock()

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_mongo_client
    mock_mongo_client.command.side_effect = raise_exception_connection_failure
    MongoClient.return_value = mock_db

    os.environ[MONGO_URI_ENV_NAME] = "mongo_uri"
    DatabaseMeta._instances.clear()
    with raises(UnexpectedDatabasePingFailed):
        Database()._ping_database_connection()
