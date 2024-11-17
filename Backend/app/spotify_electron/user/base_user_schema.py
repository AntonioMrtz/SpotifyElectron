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


def get_user_dao_from_document(document: dict[str, Any]) -> BaseUserDAO:
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


def get_user_dto_from_dao(user_dao: BaseUserDAO) -> BaseUserDTO:
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
    """Repository Unexpected error"""

    ERROR = "Error accessing BaseUser REPOSITORY"

    def __init__(self):
        super().__init__(self.ERROR)


class BaseUserNotFoundException(SpotifyElectronException):
    """BaseUser not found"""

    ERROR = "BaseUser not found"

    def __init__(self):
        super().__init__(self.ERROR)


class BaseUserBadNameException(SpotifyElectronException):
    """Bad name"""

    ERROR = "Bad parameters provided for BaseUser"

    def __init__(self):
        super().__init__(self.ERROR)


class BaseUserAlreadyExistsException(SpotifyElectronException):
    """Exception raised when a BaseUser already exists"""

    ERROR = "BaseUser already exists"

    def __init__(self):
        super().__init__(self.ERROR)


class BaseUserDeleteException(SpotifyElectronException):
    """Exception raised when there is an error deleting a BaseUser"""

    ERROR = "Error deleting BaseUser"

    def __init__(self):
        super().__init__(self.ERROR)


class BaseUserCreateException(SpotifyElectronException):
    """Exception raised when there is an error inserting a BaseUser"""

    ERROR = "Error inserting BaseUser"

    def __init__(self):
        super().__init__(self.ERROR)


class BaseUserUpdateException(SpotifyElectronException):
    """Exception raised when there is an error updating a BaseUser"""

    ERROR = "Error updating BaseUser"

    def __init__(self):
        super().__init__(self.ERROR)


class BaseUserGetPasswordException(SpotifyElectronException):
    """Exception raised when there is an error getting BaseUser password"""

    ERROR = "Error getting BaseUser password"

    def __init__(self):
        super().__init__(self.ERROR)


class BaseUserServiceException(SpotifyElectronException):
    """Exception raised when there is an unexpected error in BaseUserService"""

    ERROR = "Error accessing BaseUser Service"

    def __init__(self):
        super().__init__(self.ERROR)


class BaseUserBadParametersException(SpotifyElectronException):
    """Exception raised when bad parameters are provided for a BaseUser"""

    ERROR = "Bad parameters provided for BaseUser"

    def __init__(self):
        super().__init__(self.ERROR)
