"""
Migrate song.files collection to implement the new metadata field.

The following fields will be included in the metadata field and removed from the base document:

"artist",
"duration",
"genre",
"photo",
"streams",
"url",
"""

import asyncio

from app.database.database_schema import DatabaseCollection
from app.database.DatabaseConnectionManager import DatabaseConnectionManager
from app.scripts.migrations.base_migration import BaseMigration


class Migration(BaseMigration):
    """Migrate songs collection to include metadata field"""

    def __init__(self) -> None:
        super().__init__()

    async def up(self) -> None:
        """Include metadata field, migrate the values and remove old fields"""
        self._collection = DatabaseConnectionManager.get_collection_connection(
            collection_name=DatabaseCollection.SONG_BLOB_FILE
        )

        await self._collection.update_many(
            {},
            [
                {
                    "$set": {
                        "metadata.artist": "$artist",
                        "metadata.duration": "$duration",
                        "metadata.genre": "$genre",
                        "metadata.photo": "$photo",
                        "metadata.streams": "$streams",
                        "metadata.url": "$url",
                    }
                },
                {
                    "$unset": [
                        "artist",
                        "duration",
                        "genre",
                        "photo",
                        "streams",
                        "url",
                    ]
                },
            ],
        )

    async def down(self) -> None:
        """Remove new metadata fields and populate old fields at root level"""
        self._collection = DatabaseConnectionManager.get_collection_connection(
            collection_name=DatabaseCollection.SONG_BLOB_FILE
        )

        await self._collection.update_many(
            {},
            [
                {
                    "$set": {
                        "artist": "$metadata.artist",
                        "duration": "$metadata.duration",
                        "genre": "$metadata.genre",
                        "photo": "$metadata.photo",
                        "streams": "$metadata.streams",
                        "url": "$metadata.url",
                    }
                },
                {
                    "$unset": [
                        "metadata.artist",
                        "metadata.duration",
                        "metadata.genre",
                        "metadata.photo",
                        "metadata.streams",
                        "metadata.url",
                        "metadata",
                    ]
                },
            ],
        )


migration = Migration()
asyncio.run(migration.execute_migration())
