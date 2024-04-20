from app.exceptions.exceptions_schema import SpotifyElectronException


class InvalidCredentialsLoginException(SpotifyElectronException):
    """Exception for invalid credentials while logging"""

    ERROR = "Invalid credentials while logging"

    def __init__(self):
        super().__init__(self.ERROR)
