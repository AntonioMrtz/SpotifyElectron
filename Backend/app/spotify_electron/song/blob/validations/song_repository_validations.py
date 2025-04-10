"""Validations for song repository"""

from gridfs import GridOut

from app.spotify_electron.song.blob.song_schema import SongDataNotFoundError


def validate_song_data_exists(song_file: GridOut | None) -> None:
    """Validate song data exists

    Args:
        song_file (GridOut): song data

    Raises:
        SongDataNotFoundError: if the song data doesn't exists
    """
    if song_file is None:
        raise SongDataNotFoundError
