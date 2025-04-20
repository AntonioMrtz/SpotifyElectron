"""
Migrate songs field `duration` to `seconds_duration`
"""

import asyncio

from app.database.database_schema import DatabaseCollection
from app.database.DatabaseConnectionManager import DatabaseConnectionManager
from app.scripts.migrations.base_migration import BaseMigration


class Migration(BaseMigration):
    """Migrate songs field `duration` to `seconds_duration`"""

    def __init__(self) -> None:
        super().__init__()

    async def up(self) -> None:
        """Renames the field name if the old field name is present"""
        self._collection = DatabaseConnectionManager.get_collection_connection(
            collection_name=DatabaseCollection.SONG_BLOB_FILE
        )
        await self._collection.update_many(
            {"metadata.duration": {"$exists": True}},
            {"$rename": {"metadata.duration": "metadata.seconds_duration"}},
        )

    async def down(self) -> None:
        """Renames the field name if the new field name is present"""
        self._collection = DatabaseConnectionManager.get_collection_connection(
            collection_name=DatabaseCollection.SONG_BLOB_FILE
        )
        await self._collection.update_many(
            {"metadata.seconds_duration": {"$exists": True}},
            {"$rename": {"metadata.seconds_duration": "metadata.duration"}},
        )


migration = Migration()
asyncio.run(migration.execute_migration())
