"""
BaseUser schema
"""

from dataclasses import dataclass
from typing import Any

from app.exceptions.base_exceptions_schema import SpotifyElectronException


@dataclass
class BaseUserDAO:
    """Represents base user data in the persistence layer"""

    name: str
    photo: str
    register_date: str
    password: bytes


@dataclass
class BaseUserDTO:
    """Represents base user data in the endpoints transfer layer"""

    name: str
    photo: str
    register_date: str


def get_base_user_dao_from_document(document: dict[str, Any]) -> BaseUserDAO:
    """Get BaseUserDAO from document

    Args:
    ----
        document (dict): BaseUser document

    Returns:
    -------
        BaseUserDAO: BaseUserDAO Object

    """
    return BaseUserDAO(
        name=document["name"],
        photo=document["photo"],
        register_date=document["register_date"][:-1],
        password=document["password"],
    )


def get_base_user_dto_from_dao(user_dao: BaseUserDAO) -> BaseUserDTO:
    """Get BaseUserDTO from BaseUserDAO

    Args:
    ----
        user_dao (BaseUserDAO): BaseUserDAO object

    Returns:
    -------
        BaseUserDTO: BaseUserDTO object

    """
    return BaseUserDTO(
        name=user_dao.name,
        photo=user_dao.photo,
        register_date=user_dao.register_date,
    )


class BaseUserRepositoryException(SpotifyElectronException):
    """Base Repository Unexpected error"""

    ERROR = "Error accessing User Repository"

    def __init__(self, error: str = ERROR):
        super().__init__(error)


class BaseUserNotFoundException(SpotifyElectronException):
    """User not found"""

    ERROR = "User not found"

    def __init__(self, error: str = ERROR):
        super().__init__(error)


class BaseUserBadNameException(SpotifyElectronException):
    """Bad namefor user"""

    ERROR = "Bad parameters provided for User"

    def __init__(self, error: str = ERROR):
        super().__init__(error)


class BaseUserAlreadyExistsException(SpotifyElectronException):
    """Exception raised when user already exists"""

    ERROR = "User already exists"

    def __init__(self, error: str = ERROR):
        super().__init__(error)


class BaseUserDeleteException(SpotifyElectronException):
    """Exception raised when there is an error deleting a user"""

    ERROR = "Error deleting user"

    def __init__(self, error: str = ERROR):
        super().__init__(error)


class BaseUserCreateException(SpotifyElectronException):
    """Exception raised when there is an error inserting a user"""

    ERROR = "Error inserting user"

    def __init__(self, error: str = ERROR):
        super().__init__(error)


class BaseUserUpdateException(SpotifyElectronException):
    """Exception raised when there is an error updating a user"""

    ERROR = "Error updating user"

    def __init__(self, error: str = ERROR):
        super().__init__(error)


class BaseUserGetPasswordException(SpotifyElectronException):
    """Exception raised when there is an error getting user password"""

    ERROR = "Error getting user password"

    def __init__(self, error: str = ERROR):
        super().__init__(error)


class BaseUserServiceException(SpotifyElectronException):
    """Exception raised when there is an unexpected error in user service"""

    ERROR = "Error accessing base user Service"

    def __init__(self, error: str = ERROR):
        super().__init__(error)


class BaseUserBadParametersException(SpotifyElectronException):
    """Exception raised when bad parameters are provided for a user"""

    ERROR = "Bad parameters provided for user"

    def __init__(self, error: str = ERROR):
        super().__init__(error)
