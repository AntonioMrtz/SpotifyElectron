"""Validations for song repository"""

from gridfs import GridOut

from app.spotify_electron.song.blob.song_schema import SongDataNotFoundException


def validate_song_file_exists(song_file: GridOut | None) -> None:
    """Validate song file exists

    Args:
        song_file (GridOut): song file

    Raises:
        SongGetFileException: if the song file doesn't exists
    """
    if song_file is None:
        raise SongDataNotFoundException
