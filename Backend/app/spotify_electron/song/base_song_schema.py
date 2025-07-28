"""Base Song schema.
It contains Base DAO/DTO objects both for Metadata and Song containing
the song resource.
"""

from abc import ABC
from dataclasses import dataclass
from typing import TypedDict

from app.exceptions.base_exceptions_schema import SpotifyElectronError
from app.spotify_electron.genre.genre_schema import Genre


class BaseSongMetadataDocument(TypedDict):
    """Represents song metadata in the persistence layer"""

    photo: str
    artist: str
    seconds_duration: int
    genre: str
    streams: int


class BaseSongDocument(TypedDict):
    """Represents song data in the persistence layer"""

    filename: str
    metadata: BaseSongMetadataDocument


@dataclass
class BaseSongDAO(ABC):
    """Represents song data in the internal processing layer"""

    name: str
    photo: str
    artist: str
    seconds_duration: int
    genre: Genre
    streams: int


@dataclass
class BaseSongDTO(ABC):
    """Base song representation in the endpoints transfering layer"""

    name: str
    photo: str
    artist: str
    seconds_duration: int
    genre: Genre
    streams: int


@dataclass
class SongMetadataDAO(BaseSongDAO):
    """Represents Song metadata in the persistence transfering layer"""


@dataclass
class SongMetadataDTO(BaseSongDTO):
    """Represents Song metadata in the endpoints transfering layer"""


def get_song_metadata_dao_from_document(
    song_name: str, document: BaseSongMetadataDocument
) -> SongMetadataDAO:
    """Get SongMetadataDAO from document

    Args:
    ----
        song_name: song name
        document: song document

    Returns:
    -------
        SongMetadataDAO Object
    """
    return SongMetadataDAO(
        name=song_name,
        photo=document["photo"],
        artist=document["artist"],
        seconds_duration=document["seconds_duration"],
        genre=Genre(document["genre"]),
        streams=document["streams"],
    )


def get_song_metadata_dto_from_dao(song_dao: SongMetadataDAO) -> SongMetadataDTO:
    """Get song metadata from dao

    Args:
        song_dao: song dao

    Returns:
        the song metadata
    """
    return SongMetadataDTO(
        name=song_dao.name,
        photo=song_dao.photo,
        artist=song_dao.artist,
        seconds_duration=song_dao.seconds_duration,
        genre=song_dao.genre,
        streams=song_dao.streams,
    )


class SongRepositoryError(SpotifyElectronError):
    """Repository Unexpected error"""

    ERROR = "Error accessing Song Repository"

    def __init__(self):
        super().__init__(self.ERROR)


class SongNotFoundError(SpotifyElectronError):
    """Song not found"""

    ERROR = "Song not found"

    def __init__(self):
        super().__init__(self.ERROR)


class SongAlreadyExistsError(SpotifyElectronError):
    """Song already exists"""

    ERROR = "Song already exists"

    def __init__(self):
        super().__init__(self.ERROR)


class SongDeleteError(SpotifyElectronError):
    """Song deletion error"""

    ERROR = "Error deleting Song"

    def __init__(self):
        super().__init__(self.ERROR)


class SongCreateError(SpotifyElectronError):
    """Song creation error"""

    ERROR = "Error creating Song"

    def __init__(self):
        super().__init__(self.ERROR)


class SongtUpdateError(SpotifyElectronError):
    """Song update error"""

    ERROR = "Error updating Song"

    def __init__(self):
        super().__init__(self.ERROR)


class SongServiceError(SpotifyElectronError):
    """Song Service Unexpected error"""

    ERROR = "Error accessing Song Service"

    def __init__(self):
        super().__init__(self.ERROR)


class SongBadNameError(SpotifyElectronError):
    """Bad name"""

    ERROR = "Bad parameters provided for Song"

    def __init__(self):
        super().__init__(self.ERROR)


class SongServiceHealthCheckError(SpotifyElectronError):
    """Song service health check failure"""

    ERROR = "Song service health check failed"

    def __init__(self):
        super().__init__(self.ERROR)
