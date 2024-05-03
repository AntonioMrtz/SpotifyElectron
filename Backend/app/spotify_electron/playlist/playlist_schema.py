from dataclasses import dataclass

from app.exceptions.exceptions_schema import SpotifyElectronException


@dataclass
class PlaylistDAO:
    """A class to represent playlist data in the persistence layer"""

    name: str
    photo: str
    description: str
    upload_date: str
    owner: str
    song_names: list[str]


@dataclass
class PlaylistDTO:
    """A class to represent playlist data in the endpoints transfering layer"""

    name: str
    photo: str
    description: str
    upload_date: str
    owner: str
    song_names: list[str]


def get_playlist_dao_from_document(document: dict) -> PlaylistDAO:
    """Get PlaylistDAO from document

    Args:
    ----
        document (dict): playlist document

    Returns:
    -------
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
    ----
        playlist_dao (PlaylistDAO): PlaylistDAO object

    Returns:
    -------
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


class PlaylistRepositoryException(SpotifyElectronException):
    """Exception for Playlist Repository Unexpected Exceptions"""

    ERROR = "Error accessing Playlist Repository"

    def __init__(self):
        super().__init__(self.ERROR.format(PLAYLIST=""))


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


class PlaylistInsertException(SpotifyElectronException):
    """Exception for Playlist insert"""

    ERROR = "Error inserting Playlist"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistUpdateException(SpotifyElectronException):
    """Exception for Playlist update"""

    ERROR = "Error updating Playlist"

    def __init__(self):
        super().__init__(self.ERROR)


class PlaylistServiceException(SpotifyElectronException):
    """Exception for Playlist Service Unexpected Exceptions"""

    ERROR = "Error accessing {PLAYLIST} SERVICE"

    def __init__(self):
        super().__init__(self.ERROR.format(PLAYLIST=""))


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
