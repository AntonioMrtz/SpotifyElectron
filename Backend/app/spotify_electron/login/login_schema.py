"""
Login schema for domain model
"""

from app.exceptions.base_exceptions_schema import SpotifyElectronException


class InvalidCredentialsLoginException(SpotifyElectronException):
    """Invalid credentials for log in"""

    ERROR = "Invalid credentials while logging"

    def __init__(self):
        super().__init__(self.ERROR)
