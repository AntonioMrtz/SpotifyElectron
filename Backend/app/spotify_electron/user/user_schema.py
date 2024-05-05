from dataclasses import dataclass
from enum import Enum

from app.exceptions.exceptions_schema import SpotifyElectronException


@dataclass
class User:
    # TODO docstirng
    name: str
    photo: str
    register_date: str
    password: bytes
    playback_history: list[str]
    playlists: list[str]
    saved_playlists: list[str]


class UserType(Enum):
    """Type/roles of users"""

    ARTIST = "artist"
    USER = "user"


class UserRepositoryException(SpotifyElectronException):
    """Exception for User Repository Unexpected Exceptions"""

    def __init__(self):
        super().__init__("Error accessing User REPOSITORY")


class UserNotFoundException(SpotifyElectronException):
    """Exception for User item not found"""

    def __init__(self):
        super().__init__("User not found")
