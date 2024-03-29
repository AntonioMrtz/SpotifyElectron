from app.logging.logger_constants import LOGGING_EXCEPTION
from app.logging.logging_schema import SpotifyElectronLogger


exceptions_logger = SpotifyElectronLogger(LOGGING_EXCEPTION).getLogger()


class SpotifyElectronException(Exception):
    def __init__(self, message):
        super().__init__(message)
        exceptions_logger.critical(message)
