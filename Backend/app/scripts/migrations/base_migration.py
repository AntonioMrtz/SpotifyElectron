"""
Base class for migrations. Children classes need to implement UP and DOWN methods.

Commands:
    help: print script usage
    uri: database uri
    up|down: migration direction

Steps:
    1. Go to Backend/
    2. Create a migration file that extends `BaseMigration` class under\
          `app/scripts/migrations`
    3. Write module docs at the top of the file describing what the migration does
    4. Add the following entrypoint:
    ```
    migration = Migration()
    asyncio.run(migration.execute_migration())
    ```
    5. Run `python -m app.scripts.migration_file \
        [help | mongodb://root:root@127.0.0.1:27017/ (up|down)]`
"""

import sys
from abc import ABC, abstractmethod
from enum import StrEnum

from app.common.app_schema import AppEnvironmentMode
from app.database.DatabaseConnectionManager import DatabaseConnectionManager
from app.exceptions.base_exceptions_schema import SpotifyElectronError
from app.logging.logging_schema import SpotifyElectronLogger

LOGGING_MIGRATIONS = "MIGRATIONS"
HELP_COMMAND = "help"
MIN_AMOUNT_ARGUMENTS = 2


class MigrationDirection(StrEnum):
    """Migration direction options"""

    UP = "up"
    DOWN = "down"


class InvalidMigrationDirectionError(SpotifyElectronError):
    """Invalid migration direction"""

    ERROR = "Invalid migration direction"

    def __init__(self):
        super().__init__(self.ERROR)


class BaseMigration(ABC):
    """Base migration class"""

    def __init__(self) -> None:
        super().__init__()
        self._log = SpotifyElectronLogger(LOGGING_MIGRATIONS).get_logger()

    @staticmethod
    def _print_help() -> None:
        """Prints script usage for the migration tool"""
        print(
            "----------------------------\n"
            "MongoDB Migration Script\n"
            "\n"
            "Usage:\n"
            "  python migration_script.py <mongo_uri> <direction>\n"
            "\n"
            "Arguments:\n"
            "  <mongo_uri>    MongoDB connection string (e.g. mongodb://root:root@127.0.0.1:27017/)\n"
            "  <direction>    Migration direction: 'up' to apply changes, 'down' to revert\n"
            "\n"
            "Example:\n"
            "  python migration_script.py mongodb://localhost:27017/ up\n"
            "\n"
            "Other Commands:\n"
            "  help           Show this message\n"
            "----------------------------\n"
        )

    @abstractmethod
    async def up(self) -> None:
        """Executes the migration

        Raises:
            RuntimeError: up method is not implented
        """
        raise RuntimeError("Up method not implemented")  # noqa: TRY003

    @abstractmethod
    async def down(self) -> None:
        """Rollback the migration

        Raises:
            RuntimeError: up method is not implented
        """
        raise RuntimeError("Down method not implemented")  # noqa: TRY003

    async def execute_migration(self) -> None:
        """Executes migration based on direction

        Raises:
            InvalidMigrationDirectionError: invalid migration direction
        """
        if sys.argv[1] == HELP_COMMAND:
            self._print_help()
            return
        try:
            if len(sys.argv) <= MIN_AMOUNT_ARGUMENTS:
                print("Invalid options. Use help command")
                return

            uri = sys.argv[1]
            direction = sys.argv[2]

            await DatabaseConnectionManager.init_database_connection(
                connection_uri=uri,
                environment=AppEnvironmentMode.PROD,
            )

            if direction == MigrationDirection.UP:
                await self.up()
            elif direction == MigrationDirection.DOWN:
                await self.down()
            else:
                raise InvalidMigrationDirectionError  # noqa: TRY301
        except Exception:
            self._log.exception(f"Unexpected error executing migration {direction}")
        finally:
            DatabaseConnectionManager.close_database_connection()
