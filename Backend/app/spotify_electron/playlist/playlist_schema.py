"""Playlist schema for domain model"""

from dataclasses import dataclass
from typing import TypedDict

from app.exceptions.base_exceptions_schema import SpotifyElectronError


class PlaylistDocument(TypedDict):
    """Represents playlist data in the persistence layer"""

    name: str
    photo: str
    description: str
    upload_date: str
    owner: str
    song_names: list[str]


@dataclass
class PlaylistDAO:
    """Represents playlist data in the internal processing layer"""

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


def get_playlist_dao_from_document(document: PlaylistDocument) -> PlaylistDAO:
    """Get PlaylistDAO from document

    Args:
    ----
        document: playlist document

    Returns:
    -------
        PlaylistDAO Object
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
        playlist_dao: PlaylistDAO object

    Returns:
    -------
        PlaylistDTO object
    """
    return PlaylistDTO(
        name=playlist_dao.name,
        photo=playlist_dao.photo,
        description=playlist_dao.description,
        upload_date=playlist_dao.upload_date,
        owner=playlist_dao.owner,
        song_names=playlist_dao.song_names,
    )


class PlaylistRepositoryError(SpotifyElectronError):
    """Repository Unexpected Exceptions"""

    ERROR = "Error accessing Playlist Repository"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistNotFoundError(SpotifyElectronError):
    """Playlist not found"""

    ERROR = "Playlist not found"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistAlreadyExistsError(SpotifyElectronError):
    """Playlist to create already exists"""

    ERROR = "Playlist already exists"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistDeleteError(SpotifyElectronError):
    """Playlist deletion"""

    ERROR = "Error deleting Playlist"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistCreateError(SpotifyElectronError):
    """Playlist creation"""

    ERROR = "Error creating Playlist"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistUpdateError(SpotifyElectronError):
    """Playlist update"""

    ERROR = "Error updating Playlist"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistServiceError(SpotifyElectronError):
    """Service Unexpected Exceptions"""

    ERROR = "Error accessing Playlist SERVICE"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistBadNameError(SpotifyElectronError):
    """Bad name"""

    ERROR = "Bad parameters provided for playlist"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistUnAuthorizedError(SpotifyElectronError):
    """User accessing unauthorized playlist"""

    ERROR = "Unauthorized playlist resource for user"

    def __init__(self):
        super().__init__(self.ERROR)
