"""
Song schema for domain model
"""

from dataclasses import dataclass
from typing import Any

from app.exceptions.base_exceptions_schema import SpotifyElectronException
from app.spotify_electron.genre.genre_schema import Genre
from app.spotify_electron.song.base_song_schema import BaseSongDAO, BaseSongDTO


@dataclass
class SongDAO(BaseSongDAO):
    """Represents song data in the persistence layer"""

    url: str
    """The streaming url of the song"""


@dataclass
class SongDTO(BaseSongDTO):
    """Represents song metadata and payload in the endpoints"""

    url: str
    """The streaming url of the song"""


def get_song_dao_from_document(document: dict[str, Any]) -> SongDAO:
    """Creates a SongDAO object from a document dictionary.

    Args:
       document: Dictionary containing song data.

    Returns:
       A SongDAO object populated with the document data.
    """
    return SongDAO(
        name=document["name"],
        photo=document["photo"],
        artist=document["artist"],
        seconds_duration=document["duration"],
        genre=Genre(document["genre"]),
        streams=document["streams"],
        url=document["url"],
    )


def get_song_dto_from_dao(song_dao: SongDAO, url: str) -> SongDTO:
    """Creates a SongDTO object from a SongDAO object.

    Args:
       song_dao: The SongDAO object to convert.
       url: The song's streaming URL.

    Returns:
       A SongDTO object containing the song data.
    """
    return SongDTO(
        name=song_dao.name,
        photo=song_dao.photo,
        artist=song_dao.artist,
        seconds_duration=song_dao.seconds_duration,
        genre=song_dao.genre,
        streams=song_dao.streams,
        url=url,
    )


class SongDataNotFoundException(SpotifyElectronException):
    """Exception for getting Song data"""

    ERROR = "Error getting song data"

    def __init__(self):
        super().__init__(self.ERROR)
