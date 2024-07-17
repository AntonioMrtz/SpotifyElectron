"""
Playlist schema for domain model
"""

from dataclasses import dataclass
from typing import Any

from app.exceptions.base_exceptions_schema import SpotifyElectronException


@dataclass
class PlaylistDAO:
    """Represents playlist data in the persistence layer"""

    name: str
    photo: str
    description: str
    upload_date: str
    owner: str
    song_names: list[str]


@dataclass
class PlaylistDTO:
    """Represents playlist data in the endpoints transfer layer"""

    name: str
    photo: str
    description: str
    upload_date: str
    owner: str
    song_names: list[str]


def get_playlist_dao_from_document(document: dict[str, Any]) -> PlaylistDAO:
    """Get PlaylistDAO from document

    Args:
    ----
        document (dict): playlist document

    Returns:
    -------
        PlaylistDAO: PlaylistDAO Object
    """
    return PlaylistDAO(
        name=document["name"],
        photo=document["photo"],
        description=document["description"],
        upload_date=document["upload_date"][:-1],
        owner=document["owner"],
        song_names=document["song_names"],
    )


def get_playlist_dto_from_dao(playlist_dao: PlaylistDAO) -> PlaylistDTO:
    """Get PlaylistDTO from PlaylistDAO

    Args:
    ----
        playlist_dao (PlaylistDAO): PlaylistDAO object

    Returns:
    -------
        PlaylistDTO: PlaylistDTO object
    """
    return PlaylistDTO(
        name=playlist_dao.name,
        photo=playlist_dao.photo,
        description=playlist_dao.description,
        upload_date=playlist_dao.upload_date,
        owner=playlist_dao.owner,
        song_names=playlist_dao.song_names,
    )


class PlaylistRepositoryException(SpotifyElectronException):
    """Exception for Playlist Repository Unexpected Exceptions"""

    ERROR = "Error accessing Playlist Repository"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistNotFoundException(SpotifyElectronException):
    """Exception for Playlist item not found"""

    ERROR = "Playlist not found"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistAlreadyExistsException(SpotifyElectronException):
    """Exception for Playlist that already exists"""

    ERROR = "Playlist already exists"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistDeleteException(SpotifyElectronException):
    """Exception for Playlist delete"""

    ERROR = "Error deleting Playlist"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistCreateException(SpotifyElectronException):
    """Exception for Playlist creation"""

    ERROR = "Error creating Playlist"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistUpdateException(SpotifyElectronException):
    """Exception for Playlist update"""

    ERROR = "Error updating Playlist"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistServiceException(SpotifyElectronException):
    """Exception for Playlist Service Unexpected Exceptions"""

    ERROR = "Error accessing Playlist SERVICE"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistBadNameException(SpotifyElectronException):
    """Exception for bad name of Playlist"""

    ERROR = "Bad parameters provided for playlist"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistUnAuthorizedException(SpotifyElectronException):
    """Exception for user accessing unauthorized playlist"""

    ERROR = "Unauthorized playlist resource for user"

    def __init__(self):
        super().__init__(self.ERROR)
