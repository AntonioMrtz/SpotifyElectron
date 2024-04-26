from app.logging.logging_constants import LOGGING_EXCEPTION
from app.logging.logging_schema import SpotifyElectronLogger

exceptions_logger = SpotifyElectronLogger(LOGGING_EXCEPTION).getLogger()


class SpotifyElectronException(Exception):
    def __init__(self, message):
        super().__init__(message)


class BadParameterException(SpotifyElectronException):
    """Exception for bad parameter"""

    def __init__(self, parameter_name: str):
        self._set_parameter_name(parameter_name)
        super().__init__(self.error)

    def _set_parameter_name(self, item_name: str):
        self.error = f"Bad parameter : {item_name}"
