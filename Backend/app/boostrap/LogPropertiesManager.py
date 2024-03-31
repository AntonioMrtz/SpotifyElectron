import configparser
import os

from app.constants.config_constants import (
    APP_FOLDER,
    CONFIG_FILENAME,
    LOG_CONFIG_SECTION,
    LOG_FILE,
    RESOURCES_FOLDER,
)
from app.constants.set_up_constants import ENV_VALUE_ENV_NAME, PROD
from dotenv import load_dotenv


class _LogPropertiesManager:
    """Parses and stores enviroment and config files"""

    def __init__(self) -> None:
        load_dotenv()
        self.current_directory = os.getcwd()
        self.config_sections = [LOG_CONFIG_SECTION]
        for config_section in self.config_sections:
            self._load_config_variables(CONFIG_FILENAME, config_section)

    def _load_config_variables(self, config_filename: str, config_section: str):
        """Loads attributes from .ini file and stores them as class attributes

        Args:
            config_filename (str): the name of the config file
            config_section (str): the section inside of the config file
        """
        self.config_file = os.path.join(
            self.current_directory, APP_FOLDER, RESOURCES_FOLDER, config_filename
        )
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self._set_attributes(config_section)

    def _set_attributes(self, config_section: str):
        """Sets app atributes from .ini file into class attributes, if value its empty\
            string it will load None

        Args:
            config_section (str): the config file section to load
        """
        for key, value in self.config.items(config_section):
            if value == "":
                value = None
            setattr(self, key, value)

    def is_log_file_provided(self) -> bool:
        """Checks if theres a valid log file provided

        Returns:
            bool: Returns if theres a valid log provided
        """
        return self.__getattribute__(LOG_FILE) is not None

    def is_production_enviroment(self) -> bool:
        """Checks if the enviroment is production

        Returns:
            bool: Returns if its production enviroment
        """
        env_value = os.getenv(ENV_VALUE_ENV_NAME, PROD)
        return env_value == PROD


LogPropertiesManager = _LogPropertiesManager()
