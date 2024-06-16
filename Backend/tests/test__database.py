import os
from unittest.mock import Mock, patch

from pymongo.errors import ConnectionFailure
from pytest import raises

from app.common.set_up_constants import MONGO_URI_ENV_NAME
from app.database.Database import (
    Database,
    DatabasePingFailed,
    Singleton,
    UnexpectedDatabasePingFailed,
)


@patch("sys.exit")
@patch("app.database.Database.Database._get_mongo_client_class")
def test_raise_exception_connection_failure(
    get_mongo_client_class_mock, sys_exit_mock, clean_modified_environments
):
    def raise_exception_connection_failure(*arg):
        raise ConnectionFailure

    client_mock = Mock()
    database_connection_mock = Mock()
    database_connection_mock.command.side_effect = raise_exception_connection_failure
    client_mock.return_value = {Database.DATABASE_NAME: database_connection_mock}
    get_mongo_client_class_mock.return_value = client_mock

    os.environ[MONGO_URI_ENV_NAME] = "mongo_uri"
    Singleton._instances.clear()
    with raises(DatabasePingFailed):
        Database()._ping_database_connection()

    assert sys_exit_mock.call_count == 1
    Singleton._instances.clear()


@patch("sys.exit")
@patch("app.database.Database.Database._get_mongo_client_class")
def test_raise_exception_unexpected_connection_failure(
    get_mongo_client_class_mock, sys_exit_mock, clean_modified_environments
):
    def raise_exception_connection_failure(*arg):
        raise UnexpectedDatabasePingFailed

    client_mock = Mock()
    database_connection_mock = Mock()
    database_connection_mock.command.side_effect = raise_exception_connection_failure
    client_mock.return_value = {Database.DATABASE_NAME: database_connection_mock}
    get_mongo_client_class_mock.return_value = client_mock

    os.environ[MONGO_URI_ENV_NAME] = "mongo_uri"
    Singleton._instances.clear()
    with raises(UnexpectedDatabasePingFailed):
        Database()._ping_database_connection()

    assert sys_exit_mock.call_count == 1
    Singleton._instances.clear()
