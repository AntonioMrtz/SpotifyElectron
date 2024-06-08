"""
Base Song schema.
It contains Base DAO/DTO objects both for Metadata and Song containing
the song resource.
"""

from dataclasses import dataclass

from app.exceptions.base_exceptions_schema import SpotifyElectronException
from app.spotify_electron.genre.genre_schema import Genre


@dataclass
class BaseSongDAO:
    """Base Class to represent song data in the persistence layer"""

    name: str
    photo: str
    artist: str
    seconds_duration: int
    genre: Genre
    number_of_playbacks: list[str]


@dataclass
class BaseSongDTO:
    """Base Class to represent song data in the endpoints transfering layer"""

    name: str
    photo: str
    artist: str
    seconds_duration: int
    genre: Genre
    number_of_playbacks: list[str]


@dataclass
class SongMetadataDAO(BaseSongDAO):
    """Class to represent Song metadata in the persistence transfering layer"""


@dataclass
class SongMetadataDTO(BaseSongDTO):
    """Class to represent Song metadata in the endpoints transfering layer"""


def get_song_metadata_dao_from_document(document: dict) -> SongMetadataDAO:
    """Get SongMetadataDAO from document

    Args:
    ----
        document (dict): song document

    Returns:
    -------
        SongMetadataDAO: SongMetadataDAO Object

    """
    return SongMetadataDAO(
        name=document["name"],
        photo=document["photo"],
        artist=document["artist"],
        seconds_duration=document["duration"],
        genre=Genre(document["genre"]),
        number_of_playbacks=document["number_of_playbacks"],
    )


def get_song_metadata_dto_from_dao(song_dao: SongMetadataDAO) -> SongMetadataDTO:
    """Get song metadata from dao

    Args:
        song_dao (SongMetadataDAO): song dao

    Returns:
        SongMetadataDTO: the song metadata
    """
    return SongMetadataDTO(
        name=song_dao.name,
        photo=song_dao.photo,
        artist=song_dao.artist,
        seconds_duration=song_dao.seconds_duration,
        genre=song_dao.genre,
        number_of_playbacks=song_dao.number_of_playbacks,
    )


class SongRepositoryException(SpotifyElectronException):
    """Exception for Song Repository Unexpected Exceptions"""

    ERROR = "Error accessing Song Repository"

    def __init__(self):
        super().__init__(self.ERROR)


class SongNotFoundException(SpotifyElectronException):
    """Exception for Song item not found"""

    ERROR = "Song not found"

    def __init__(self):
        super().__init__(self.ERROR)


class SongAlreadyExistsException(SpotifyElectronException):
    """Exception for Song that already exists"""

    ERROR = "Song already exists"

    def __init__(self):
        super().__init__(self.ERROR)


class SongDeleteException(SpotifyElectronException):
    """Exception for Song delete"""

    ERROR = "Error deleting Song"

    def __init__(self):
        super().__init__(self.ERROR)


class SongCreateException(SpotifyElectronException):
    """Exception for Song creation"""

    ERROR = "Error creating Song"

    def __init__(self):
        super().__init__(self.ERROR)


class SongtUpdateException(SpotifyElectronException):
    """Exception for Song update"""

    ERROR = "Error updating Song"

    def __init__(self):
        super().__init__(self.ERROR)


class SongServiceException(SpotifyElectronException):
    """Exception for Song Service Unexpected Exceptions"""

    ERROR = "Error accessing Song SERVICE"

    def __init__(self):
        super().__init__(self.ERROR)


class SongBadNameException(SpotifyElectronException):
    """Exception for bad name of Song"""

    ERROR = "Bad parameters provided for Song"

    def __init__(self):
        super().__init__(self.ERROR)


class SongUnAuthorizedException(SpotifyElectronException):
    """Exception for user accessing unauthorized Song"""

    ERROR = "Unauthorized Song resource for user"

    def __init__(self):
        super().__init__(self.ERROR)
