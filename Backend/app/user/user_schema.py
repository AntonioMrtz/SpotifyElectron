from app.constants.domain_constants import USER
from app.exceptions.exceptions_schema import SpotifyElectronException


class UserRepositoryException(SpotifyElectronException):
    """Exception for User Repository Unexpected Exceptions"""

    def __init__(self):
        super().__init__(f"Error accessing {USER} REPOSITORY")


class UserNotFoundException(SpotifyElectronException):
    """Exception for User item not found"""

    def __init__(self):
        super().__init__("User not found")
