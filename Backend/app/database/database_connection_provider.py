"""Database connection provider"""

from app.common.app_schema import AppEnvironmentMode
from app.database.database_schema import BaseDatabaseConnection
from app.database.DatabaseProductionConnection import DatabaseProductionConnection
from app.database.DatabaseTestingConnection import DatabaseTestingConnection

database_connection_mapping = {
    AppEnvironmentMode.PROD: DatabaseProductionConnection,
    AppEnvironmentMode.DEV: DatabaseProductionConnection,
    AppEnvironmentMode.TEST: DatabaseTestingConnection,
}


def init_database_connection(current_enviroment: AppEnvironmentMode) -> None:
    """Initializes the database connection and loads its unique instance\
         based on current enviroment value

    Args:
        current_enviroment (Enviroment): the current enviroment value
    """
    global database_connection
    database_connection_class = database_connection_mapping.get(
        current_enviroment, DatabaseProductionConnection
    )
    database_connection_class()
    DatabaseConnection.set_database_connection(database_connection_class)


class DatabaseConnection:
    """Database connection"""

    connection_instance: BaseDatabaseConnection = None  # type: ignore

    @classmethod
    def set_database_connection(cls, connection_instance: BaseDatabaseConnection):
        """Set database connection class attribute

        Args:
            connection_instance (BaseDatabaseConnection): the database connection instance
        """
        cls.connection_instance = connection_instance
