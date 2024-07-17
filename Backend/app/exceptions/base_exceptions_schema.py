"""
Base common exceptions for the whole app
"""

from app.logging.logging_constants import LOGGING_EXCEPTION
from app.logging.logging_schema import SpotifyElectronLogger

exceptions_logger = SpotifyElectronLogger(LOGGING_EXCEPTION).getLogger()


class SpotifyElectronException(Exception):
    """Base app exception, all exceptions must inherit from it"""

    def __init__(self, message: str):
        super().__init__(message)


class BadParameterException(SpotifyElectronException):
    """Exception for bad parameter"""

    def __init__(self, parameter_name: str):
        self._set_parameter_name(parameter_name)
        super().__init__(self.error)

    def _set_parameter_name(self, item_name: str):
        self.error = f"Bad parameter : {item_name}"


class JsonEncodeException(SpotifyElectronException):
    """Exception for error encoding object into json"""

    ERROR = "Error encoding object into json"

    def __init__(self):
        super().__init__(self.ERROR)
