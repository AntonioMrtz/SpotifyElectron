"""
Constants for Song services
"""

from enum import StrEnum


class SongServicePath(StrEnum):
    """Song service file paths"""

    MODULE_PREFIX = "app.spotify_electron.song."
    SERVERLESS_MODULE_NAME = f"{MODULE_PREFIX}serverless.song_service"
    BLOB_MODULE_NAME = f"{MODULE_PREFIX}blob.song_service"
