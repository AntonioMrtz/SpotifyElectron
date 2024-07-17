"""
Manages APP global messages, storing and making them accesible across the app

Declares _PropertiesMessagesManager global object to be accessed from across the app
"""

import configparser
import os
import re

from app.exceptions.base_exceptions_schema import SpotifyElectronException
from app.logging.logging_constants import LOGGING_PROPERTIES_MESSAGES_MANAGER
from app.logging.logging_schema import SpotifyElectronLogger

properties_messages_manager_logger = SpotifyElectronLogger(
    LOGGING_PROPERTIES_MESSAGES_MANAGER
).getLogger()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROPERTIES_INI_FILE_PATH = os.path.join(CURRENT_DIR, "../resources/messages.ini")


class _PropertiesMessagesManager:
    def __init__(self):
        # Load properties from file
        config = configparser.ConfigParser()
        config.optionxform = lambda optionstr: optionstr
        config.read(PROPERTIES_INI_FILE_PATH)

        for section in config.sections():
            for option in config.options(section):
                value = str(config[section][option])

                # Convert option to camelCase with dots
                option = re.sub(r"\.([a-z])", lambda match: match.group(1).upper(), option)
                setattr(self, option, value)

    def __iter__(self):
        pass

    def __getattr__(self, name: str) -> None:
        # Check if attribute exists with original name
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            pass

        # Convert attribute name to camelCase with dots
        new_name = re.sub(r"\.([a-z])", lambda match: match.group(1).upper(), name)

        # Check if attribute exists with new name
        try:
            return object.__getattribute__(self, new_name)
        except AttributeError as exception:
            properties_messages_manager_logger.exception(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )
            raise MessageNotFoundException from exception


class MessageNotFoundException(SpotifyElectronException):
    """Exception for message not found in PropertiesMessagesManager"""

    ERROR = "Error getting message from PropertiesMessagesManager, it doesnt exists"

    def __init__(self):
        super().__init__(self.ERROR)


PropertiesMessagesManager = _PropertiesMessagesManager()
