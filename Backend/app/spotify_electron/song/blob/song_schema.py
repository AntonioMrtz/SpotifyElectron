"""Song schema for domain model"""

from dataclasses import dataclass

from app.exceptions.base_exceptions_schema import SpotifyElectronError
from app.spotify_electron.genre.genre_schema import Genre
from app.spotify_electron.song.base_song_schema import (
    BaseSongDAO,
    BaseSongDocument,
    BaseSongDTO,
    BaseSongMetadataDocument,
)


class SongMetadataDocument(BaseSongMetadataDocument):
    """Represents song metadata in the persistence layer"""

    url: str


class SongDocument(BaseSongDocument):
    """Represents song data in the persistence layer"""

    metadata: SongMetadataDocument


@dataclass
class SongDAO(BaseSongDAO):
    """Represents song data in the internal processing layer"""

    url: str
    """The streaming url of the song"""


@dataclass
class SongDTO(BaseSongDTO):
    """Represents song metadata and payload in the endpoints"""

    url: str
    """The streaming url of the song"""


def get_song_dao_from_document(song_name: str, document: SongMetadataDocument) -> SongDAO:
    """Get SongDAO from document

    Args:
        song_name: song name
        document: song document

    Returns:
        SongDAO Object
    """
    return SongDAO(
        name=song_name,
        photo=document["photo"],
        artist=document["artist"],
        seconds_duration=document["seconds_duration"],
        genre=Genre(document["genre"]),
        streams=document["streams"],
        url=document["url"],
    )


def get_song_dto_from_dao(song_dao: SongDAO, url: str) -> SongDTO:
    """Get SongDTO from SongDAO

    Args:
    ----
        song_dao: SongDAO object
        url: song streaming url

    Returns:
    -------
        SongDTO object
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


class SongDataNotFoundError(SpotifyElectronError):
    """Exception for getting Song data"""

    ERROR = "Error getting song data"

    def __init__(self):
        super().__init__(self.ERROR)
