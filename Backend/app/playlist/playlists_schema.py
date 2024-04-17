from dataclasses import dataclass

from app.constants.domain_constants import PLAYLIST
from app.exceptions.exceptions_schema import SpotifyElectronException


@dataclass
class PlaylistDAO:
    name: str
    photo: str
    description: str
    upload_date: str
    owner: str
    song_names: list[str]


@dataclass
class PlaylistDTO:
    name: str
    photo: str
    description: str
    upload_date: str
    owner: str
    song_names: list[str]


def get_playlist_dao_from_document(document: dict) -> PlaylistDAO:
    """Get PlaylistDAO from document

    Args:
        document (dict): playlist document

    Returns:
        PlaylistDAO: PlaylistDAO Object
    """
    return PlaylistDAO(
        document["name"],
        document["photo"],
        document["description"],
        document["upload_date"][:-1],
        document["owner"],
        document["song_names"],
    )


def get_playlist_dto_from_dao(playlist_dao: PlaylistDAO) -> PlaylistDTO:
    """Get PlaylistDTO from PlaylistDAO

    Args:
        playlist_dao (PlaylistDAO): PlaylistDAO object

    Returns:
        PlaylistDTO: PlaylistDTO object
    """
    return PlaylistDTO(
        playlist_dao.name,
        playlist_dao.photo,
        playlist_dao.description,
        playlist_dao.upload_date,
        playlist_dao.owner,
        playlist_dao.song_names,
    )


"""===================== EXCEPTIONS ====================="""


class PlaylistRepositoryException(SpotifyElectronException):
    """Exception for Playlist Repository Unexpected Exceptions"""

    def __init__(self):
        super().__init__(f"Error accessing {PLAYLIST} REPOSITORY")


class PlaylistNotFoundException(SpotifyElectronException):
    """Exception for Playlist item not found"""

    def __init__(self):
        super().__init__("Playlist not found")


class PlaylistAlreadyExistsException(SpotifyElectronException):
    """Exception for Playlist that already exists"""

    def __init__(self):
        super().__init__("Playlist already exists")


class PlaylistDeleteException(SpotifyElectronException):
    """Exception for Playlist delete"""

    def __init__(self):
        super().__init__("Error deleting Playlist")


class PlaylistInsertException(SpotifyElectronException):
    """Exception for Playlist insert"""

    def __init__(self):
        super().__init__("Error inserting Playlist")

class PlaylistUpdateException(SpotifyElectronException):
    """Exception for Playlist update"""

    def __init__(self):
        super().__init__("Error updating Playlist")

class PlaylistServiceException(SpotifyElectronException):
    """Exception for Playlist Service Unexpected Exceptions"""

    def __init__(self):
        super().__init__(f"Error accessing {PLAYLIST} SERVICE")


class PlaylistBadNameException(SpotifyElectronException):
    """Exception for bad name of Playlist"""

    def __init__(self):
        super().__init__("Bad parameters provided for playlist")


class PlaylistUnAuthorizedException(SpotifyElectronException):
    """Exception for user accesing unauthorized playlist"""

    def __init__(self):
        super().__init__("Unauthorized playlist resource for user")
