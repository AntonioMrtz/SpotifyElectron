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


@dataclass
class SongDTO(BaseSongDTO):
    """Represents song metadata and payload in the endpoints"""

    """The streaming url of the song"""
    url: str


def get_song_dao_from_document(document: dict[str, Any]) -> SongDAO:
    """Creates a SongDAO object from a document dictionary.

    Args:
       document (dict): Dictionary containing song data.

    Returns:
       SongDAO: A SongDAO object populated with the document data.
    """
    return SongDAO(
        name=document["name"],
        photo=document["photo"],
        artist=document["artist"],
        seconds_duration=document["duration"],
        genre=Genre(document["genre"]),
        streams=document["streams"],
    )


def get_song_dto_from_dao(song_dao: SongDAO, url: str) -> SongDTO:
    """Converts a SongDAO object to a SongDTO object.

    Args:
       song_dao (SongDAO): The SongDAO object to convert.
       url (str): The song's streaming URL.

    Returns:
       SongDTO: A SongDTO object containing the song data.
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


class SongGetUrlStreamingException(SpotifyElectronException):
    """Get Song url for streaming error"""

    ERROR = "Unexpected error getting streaming url of Song"

    def __init__(self):
        super().__init__(self.ERROR)


class SongCreateSongStreamingException(SpotifyElectronException):
    """Song creation"""

    ERROR = "Unexpected error creating Song"

    def __init__(self):
        super().__init__(self.ERROR)


class SongDeleteSongStreamingException(SpotifyElectronException):
    """Song deletion"""

    ERROR = "Unexpected error deleting Song"

    def __init__(self):
        super().__init__(self.ERROR)
