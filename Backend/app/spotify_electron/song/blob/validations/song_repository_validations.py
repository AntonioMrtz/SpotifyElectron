"""Validations for song repository"""

from motor.motor_asyncio import AsyncIOMotorGridOut

from app.spotify_electron.song.blob.song_schema import SongDataNotFoundError


def validate_song_data_exists(song_file: AsyncIOMotorGridOut | None) -> None:
    """Validate song data exists

    Args:
        song_file: song data

    Raises:
        SongDataNotFoundError: song data doesn't exists
    """
    if song_file is None:
        raise SongDataNotFoundError
