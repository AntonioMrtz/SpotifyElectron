"""
Loads and manages logging configurations
"""

import configparser
import os

from dotenv import load_dotenv

from app.common.app_schema import (
    AppConfig,
)


class LogPropertiesManager:
    """Parses and stores environment and config files"""

    def __init__(self) -> None:
        load_dotenv()
        self.current_directory = os.getcwd()
        self.config_sections = [AppConfig.LOG_INI_SECTION]
        for config_section in self.config_sections:
            self._load_config_variables(AppConfig.CONFIG_FILENAME, config_section)

    def _load_config_variables(self, config_filename: str, config_section: str) -> None:
        """Loads config (.ini) file values into class attributes.

        Args:
           config_filename (str): Name of the config file to load.
           config_section (str): Section within the config file to process.
        """
        self.config_file = os.path.join(
            self.current_directory,
            AppConfig.APP_FOLDER,
            AppConfig.RESOURCE_FOLDER,
            config_filename,
        )
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self._set_attributes(config_section)

    def _set_attributes(self, config_section: str) -> None:
        """Sets config (.ini) file values as class attributes or None if no attribute found.

        Args:
           config_section (str): The section of the config file to load into attributes.
        """
        for key, value in self.config.items(config_section):
            if value == "":
                value = None
            setattr(self, key, value)

    def is_log_file_provided(self) -> bool:
        """Checks if a valid log file exists.

        Returns:
           bool: True if a valid log file is provided, False otherwise.
        """
        return self.__getattribute__(AppConfig.LOG_INI_FILE) is not None
