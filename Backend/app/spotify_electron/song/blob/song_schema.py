"""
Song schema for domain model
"""

from dataclasses import dataclass
from typing import Any

from gridfs.grid_file import GridOut

from app.exceptions.base_exceptions_schema import SpotifyElectronException
from app.spotify_electron.genre.genre_schema import Genre
from app.spotify_electron.song.base_song_schema import BaseSongDAO, BaseSongDTO
from app.spotify_electron.utils.audio_management.audio_management_utils import (
    EncodingFileException,
    encode_file,
)


@dataclass
class SongDAO(BaseSongDAO):
    """Represents song data in the persistence layer"""

    file: str
    """Base 64 encoded bytes of the song file"""

    def __str__(self):
        # Ensuring the string representation does not log the file attribute
        return "SongDAO(file=<Base64 encoded data>)"


@dataclass
class SongDTO(BaseSongDTO):
    """Represents song metadata and payload in the endpoints"""

    file: str
    """Base 64 encoded bytes of the song file"""

    def __str__(self):
        # Ensuring the string representation does not log the file attribute
        return "SongDAO(file=<Base64 encoded data>)"


def get_song_dao_from_document(document: dict[str, Any], song_data: GridOut) -> SongDAO:
    """Get SongDAO from document

    Args:
    ----
        document (dict): song document
        song_data (GridOut) : song data given by GridFs

    Returns:
    -------
        SongDAO: SongDAO Object
    """
    song_name = document["name"]
    encoded_song_bytes = _get_song_base64_encoded_bytes_from_gridfs(song_name, song_data)
    return SongDAO(
        name=song_name,
        photo=document["photo"],
        artist=document["artist"],
        seconds_duration=document["duration"],
        genre=Genre(document["genre"]),
        streams=document["streams"],
        file=encoded_song_bytes,
    )


def get_song_dto_from_dao(song_dao: SongDAO) -> SongDTO:
    """Get SongDTO from SongDAO

    Args:
    ----
        song_dao (SongDAO): SongDAO object

    Returns:
    -------
        SongDTO: SongDTO object

    """
    return SongDTO(
        name=song_dao.name,
        photo=song_dao.photo,
        artist=song_dao.artist,
        seconds_duration=song_dao.seconds_duration,
        genre=song_dao.genre,
        streams=song_dao.streams,
        file=song_dao.file,
    )


def _get_song_base64_encoded_bytes_from_gridfs(song_name: str, song_data: GridOut) -> str:
    """Get song bytes encoded in base64 ready for HTTP transfer from GridFs

    Args:
        song_name (str): song name
        song_data (GridOut): song data given by GridFs

    Raises:
        GetEncodedBytesFromGridFSException: unexpected error getting base 64 encoded\
              song bytes from GridFS

    Returns:
        str: the base64 encoded song bytes
    """
    try:
        song_bytes = song_data.read()
        return encode_file(song_name, song_bytes)

    except (EncodingFileException, Exception) as exception:
        raise GetEncodedBytesFromGridFSException from exception


class GetEncodedBytesFromGridFSException(SpotifyElectronException):
    """Exception for an error getting encoded bytes from GridFs"""

    ERROR = "Error getting encoded bytes from GridFs"

    def __init__(self):
        super().__init__(self.ERROR)
