from app.exceptions.exceptions_schema import SpotifyElectronException


class UserRepositoryException(SpotifyElectronException):
    """Exception for User Repository Unexpected Exceptions"""

    def __init__(self):
        super().__init__("Error accessing User REPOSITORY")


class UserNotFoundException(SpotifyElectronException):
    """Exception for User item not found"""

    def __init__(self):
        super().__init__("User not found")
