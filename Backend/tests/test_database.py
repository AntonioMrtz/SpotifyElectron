import os
from unittest.mock import MagicMock, Mock, patch

from pytest import raises
from app.constants.set_up_constants import MONGO_URI_ENV_NAME
from app.database.Database import Database, DatabaseMeta, DatabasePingFailed


@patch("app.database.Database.MongoClient")
def test_prueba(MongoClient, clean_modified_environments):
    def raise_exception():
        raise Exception("Simulated exception")

    prueba = Mock()

    # Mock the MongoClient instance and its behavior
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = prueba
    prueba.command.side_effect = raise_exception
    MongoClient.return_value = mock_db

    os.environ[MONGO_URI_ENV_NAME] = "mongo_uri"
    DatabaseMeta._instances.clear()
    with raises(DatabasePingFailed):
        Database()._ping_database_connection()
