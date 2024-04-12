import logging
import sys
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler

from app.boostrap.LogPropertiesManager import LogPropertiesManager
from app.constants.config_constants import LOG_FILE, LOG_LEVEL
from app.logging.logger_constants import DEBUG, INFO


class SpotifyElectronFormatter(Formatter):
    FORMATS = {
        logging.DEBUG: (
            "%(asctime)s - %(name)s - \033[94m%(levelname)s\033[0m - %(message)s"
        ),
        logging.INFO: (
            "%(asctime)s - %(name)s - \033[92m%(levelname)s\033[0m - %(message)s"
        ),
        logging.WARNING: (
            "%(asctime)s - %(name)s - \033[93m%(levelname)s\033[0m - %(message)s"
        ),
        logging.ERROR: (
            "%(asctime)s - %(name)s - \033[91m%(levelname)s\033[0m - %(message)s"
        ),
        logging.CRITICAL: (
            "%(asctime)s - %(name)s - \033[95m%(levelname)s\033[0m - %(message)s"
        ),
    }

    def format(self, record):
        log_format = self.FORMATS.get(
            record.levelno, "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        formatter = logging.Formatter(log_format)
        return formatter.format(record)


class SpotifyElectronLogger:
    """Custom Logger that accepts the current file logger name and\
        optionally an log file to store logs"""

    _log_properties_manager = LogPropertiesManager()

    def __init__(self, logger_name, log_file=None):
        # borg pattern shared stated
        self.log_properties_manager = SpotifyElectronLogger._log_properties_manager

        # Disable other loggers
        logging.getLogger().handlers.clear()
        logging.getLogger().propagate = False
        self._log_level_mapping = {INFO: logging.INFO, DEBUG: logging.DEBUG}

        self.logger = logging.getLogger(logger_name)

        self.logger.setLevel(self._get_log_level())
        self._manage_file_handler()
        self._manage_console_handler()

    def _manage_file_handler(self):
        """Adds logging handler depending if log file has been provided or not"""
        if not self.log_properties_manager.is_log_file_provided():
            return
        file_log_handler = RotatingFileHandler(
            self.log_properties_manager.__getattribute__(LOG_FILE),
            maxBytes=50000,
            backupCount=5,
        )
        self._add_handler(file_log_handler)

    def _manage_console_handler(self):
        """Adds logging console handler"""
        stream_handler = StreamHandler(sys.stdout)
        self._add_handler(stream_handler)

    def _add_handler(self, handler: StreamHandler | RotatingFileHandler):
        """Add handler to logger

        Args:
            handler (Union[StreamHandler, RotatingFileHandler]): the handler to add
        """

        handler.setLevel(self._get_log_level())
        formatter = SpotifyElectronFormatter()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _get_log_level(self) -> int:
        try:
            log_level = self.log_properties_manager.__getattribute__(LOG_LEVEL)
            if log_level is None:
                return logging.INFO
            mapped_log_level = self._log_level_mapping[log_level]
            return mapped_log_level
        except Exception:
            return logging.INFO

    def getLogger(self):
        return self.logger
