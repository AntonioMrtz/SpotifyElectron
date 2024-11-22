"""
Manages APP global state variables and manages initialization of\
      environment variables and .ini files

Declares PropertiesManager global object to be accessed from across the app
"""

import configparser
import os

from dotenv import load_dotenv

from app.common.app_schema import (
    AppConfig,
    AppEnvironment,
    AppEnvironmentMode,
)
from app.logging.logging_constants import LOGGING_PROPERTIES_MANAGER
from app.logging.logging_schema import SpotifyElectronLogger

properties_manager_logger = SpotifyElectronLogger(LOGGING_PROPERTIES_MANAGER).getLogger()


class _PropertiesManager:
    """Parses and stores environment and config files"""

    def __init__(self) -> None:
        properties_manager_logger.info("Initializing PropertiesManager")
        load_dotenv()
        self.current_directory = os.getcwd()
        self.config_sections = [AppConfig.APP_INI_SECTION]
        self.env_variables = [
            AppEnvironment.MONGO_URI_ENV_NAME,
            AppEnvironment.SERVERLESS_URL_ENV_NAME,
            AppEnvironment.ENV_VALUE_ENV_NAME,
        ]
        self._load_env_variables(self.env_variables)
        self._load_architecture()
        for config_section in self.config_sections:
            self._load_config_variables(AppConfig.CONFIG_FILENAME, config_section)

    def _load_config_variables(self, config_filename: str, config_section: str) -> None:
        """Loads config (.ini) file  values into class attributes.

        Args:
            config_filename (str): Name of the configuration file to load.
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
            config_section (str): The section name in the config file to load.
        """
        for key, value in self.config.items(config_section):
            if value == "":
                value = None
                properties_manager_logger.warning(f"Using None for {key} in {config_section}")
            setattr(self, key, value)

    def _load_architecture(self) -> None:
        """Loads the current architecture from environment and stores it as an\
        attribute, if none is provided DEFAULT_ARCHITECTURE will be selected
        """
        architecture_type = os.getenv(AppEnvironment.ARCHITECTURE_ENV_NAME)
        if not architecture_type:
            architecture_type = AppEnvironment.DEFAULT_ARCHITECTURE
            properties_manager_logger.warning(
                f"No architecture type selected, using {AppEnvironment.DEFAULT_ARCHITECTURE}"
            )
        self.__setattr__(AppEnvironment.ARCHITECTURE_ENV_NAME, architecture_type)
        properties_manager_logger.info(f"Architecture selected: {architecture_type}")

    def _load_env_variables(self, env_names: list[str]) -> None:
        """Loads environment variables as class attributes.

        Args:
            env_names (List[str]): List of environment variable names to load.
        """
        loaded_envs = []
        for env_name in env_names:
            env_variable_value = os.getenv(env_name)
            if not env_variable_value:
                properties_manager_logger.warning(
                    f"No environment variable provided for {env_name}"
                )
                continue
            self.__setattr__(env_name, env_variable_value)
            loaded_envs.append(env_name)
        properties_manager_logger.info(f"Environment variables loaded: {loaded_envs}")

    def get_environment(self) -> AppEnvironmentMode:
        """Get current environment

        Returns:
            environment: the current selected environment
        """
        return self.__getattribute__(AppEnvironment.ENV_VALUE_ENV_NAME)

    def is_production_environment(self) -> bool:
        """Checks if running in a production environment.

        Returns:
            bool: True if in production environment, False otherwise.
        """
        return (
            self.__getattribute__(AppEnvironment.ENV_VALUE_ENV_NAME) == AppEnvironmentMode.PROD
        )

    def is_development_environment(self) -> bool:
        """Checks if running in a development environment.

        Returns:
            bool: True if in development environment, False otherwise.
        """
        return (
            self.__getattribute__(AppEnvironment.ENV_VALUE_ENV_NAME) == AppEnvironmentMode.DEV
        )

    def is_testing_environment(self) -> bool:
        """Checks if running in a testing environment.

        Returns:
            bool: True if in testing environment, False otherwise.
        """
        return (
            self.__getattribute__(AppEnvironment.ENV_VALUE_ENV_NAME) == AppEnvironmentMode.TEST
        )

    def is_log_file_provided(self) -> bool:
        """Checks if a valid log file exists.

        Returns:
            bool: True if a valid log file is provided, False otherwise.
        """
        return self.__getattribute__(AppConfig.LOG_INI_FILE) is not None


PropertiesManager = _PropertiesManager()
