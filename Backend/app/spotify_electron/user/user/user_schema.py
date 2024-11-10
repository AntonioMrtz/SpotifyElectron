"""
Song schema for User domain model
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any

from app.spotify_electron.user.base_user_schema import BaseUserDAO, BaseUserDTO
from app.exceptions.base_exceptions_schema import SpotifyElectronException



@dataclass
class UserDAO(BaseUserDAO):
    """Represents  user data in the persistence layer"""

    playback_history: list[str]
    playlists: list[str]
    saved_playlists: list[str]


@dataclass
class UserDTO(BaseUserDTO):
    """Represents user data in the endpoints transfer layer"""

    playback_history: list[str]
    playlists: list[str]
    saved_playlists: list[str]


class UserType(Enum):
    """Type/roles of users"""

    ARTIST = "artist"
    USER = "user"


def get_user_dao_from_document(document: dict[str, Any]) -> UserDAO:
    """Get UserDAO from document by extracting all required fields.

    Args:
        document (dict): The user document.

    Returns:
        UserDAO: A fully populated UserDAO object.
    """
    return UserDAO(
        name=document["name"],
        photo=document["photo"],
        register_date=document["register_date"],
        password=document["password"],
        playback_history=document.get("playback_history", []),
        playlists=document.get("playlists", []),
        saved_playlists=document.get("saved_playlists", []),
    )


def get_user_dto_from_dao(user_dao: UserDAO) -> UserDTO:
    """Convert UserDAO to UserDTO for data transfer.

    Args:
        user_dao (UserDAO): UserDAO object to convert.

    Returns:
        UserDTO: Converted UserDTO object.
    """
    return UserDTO(
        name=user_dao.name,
        photo=user_dao.photo,
        register_date=user_dao.register_date,
        playback_history=user_dao.playback_history,
        playlists=user_dao.playlists,
        saved_playlists=user_dao.saved_playlists,
    )



class UserRepositoryException(SpotifyElectronException):
    """Repository Unexpected error"""

    def __init__(self):
        super().__init__("Error accessing User REPOSITORY")


class UserNotFoundException(SpotifyElectronException):
    """User not found"""

    def __init__(self):
        super().__init__("User not found")


class UserBadNameException(SpotifyElectronException):
    """Bad name"""

    ERROR = "Bad parameters provided for user"

    def __init__(self):
        super().__init__(self.ERROR)


class UserAlreadyExistsException(SpotifyElectronException):
    """Exception raised when a User already exists"""

    def __init__(self):
        super().__init__("User already exists")


class UserDeleteException(SpotifyElectronException):
    """Exception raised when there is an error deleting a User"""

    def __init__(self):
        super().__init__("Error deleting User")


class UserCreateException(SpotifyElectronException):
    """Exception raised when there is an error inserting a User"""

    def __init__(self):
        super().__init__("Error inserting User")


class UserUpdateException(SpotifyElectronException):
    """Exception raised when there is an error updating a User"""

    def __init__(self):
        super().__init__("Error updating User")


class UserGetPasswordException(SpotifyElectronException):
    """Exception raised when there is an error getting user password"""

    def __init__(self):
        super().__init__("Error getting User password")


class UserServiceException(SpotifyElectronException):
    """Exception raised when there is an unexpected error in UserService"""

    def __init__(self):
        super().__init__("Error accessing User Service")


class UserBadParametersException(SpotifyElectronException):
    """Exception raised when bad parameters are provided for a User"""

    def __init__(self):
        super().__init__("Bad parameters provided for User")
