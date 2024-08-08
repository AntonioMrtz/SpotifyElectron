"""
Manages APP global state variables and manages initialization of\
      enviroment variables and .ini files

Declares PropertiesManager global object to be accessed from across the app
"""

import configparser
import os

from dotenv import load_dotenv

from app.common.app_schema import (
    AppConfig,
    AppEnviroment,
    AppEnvironmentMode,
)
from app.logging.logging_constants import LOGGING_PROPERTIES_MANAGER
from app.logging.logging_schema import SpotifyElectronLogger

properties_manager_logger = SpotifyElectronLogger(LOGGING_PROPERTIES_MANAGER).getLogger()


class _PropertiesManager:
    """Parses and stores enviroment and config files"""

    def __init__(self) -> None:
        properties_manager_logger.info("Initializing PropertiesManager")
        load_dotenv()
        self.current_directory = os.getcwd()
        self.config_sections = [AppConfig.APP_INI_SECTION]
        self.env_variables = [
            AppEnviroment.MONGO_URI_ENV_NAME,
            AppEnviroment.SECRET_KEY_SIGN_ENV_NAME,
            AppEnviroment.SERVERLESS_FUNCTION_URL_ENV_NAME,
            AppEnviroment.ENV_VALUE_ENV_NAME,
        ]
        self._load_env_variables(self.env_variables)
        self._load_architecture()
        for config_section in self.config_sections:
            self._load_config_variables(AppConfig.CONFIG_FILENAME, config_section)

    def _load_config_variables(self, config_filename: str, config_section: str):
        """Loads attributes from .ini file and stores them as class attributes

        Args:
        ----
            config_filename (str): the name of the config file
            config_section (str): the section inside of the config file

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

    def _set_attributes(self, config_section: str):
        """Sets app atributes from .ini file into class attributes,\
            if value its empty string it will load None

        Args:
        ----
            config_section (str): the config file section to load

        """
        for key, value in self.config.items(config_section):
            if value == "":
                value = None
                properties_manager_logger.warning(f"Using None for {key} in {config_section}")
            setattr(self, key, value)

    def _load_architecture(self):
        """Loads the current architecture from enviroment and stores it as an\
        attribute, if none is provided DEFAULT_ARCHITECTURE will be selected
        """
        architecture_type = os.getenv(AppEnviroment.ARCHITECTURE_ENV_NAME)
        if not architecture_type:
            architecture_type = AppEnviroment.DEFAULT_ARCHITECTURE
            properties_manager_logger.warning(
                f"No architecture type selected, using {AppEnviroment.DEFAULT_ARCHITECTURE}"
            )
        self.__setattr__(AppEnviroment.ARCHITECTURE_ENV_NAME, architecture_type)
        properties_manager_logger.info(f"Architecture selected : {architecture_type}")

    def _load_env_variables(self, env_names: list[str]):
        """Load enviroment variables into class attributes

        Args:
        ----
            env_names (List[str]): enviroment variables names

        """
        for env_name in env_names:
            env_variable_value = os.getenv(env_name)
            if not env_variable_value:
                properties_manager_logger.warning(
                    f"No enviroment variable provided for {env_name}"
                )
                env_names.remove(env_name)
                continue
            self.__setattr__(env_name, env_variable_value)
        properties_manager_logger.info(f"Enviroment variables loaded : {env_names}")

    def get_enviroment(self) -> AppEnvironmentMode:
        """Get current enviroment

        Returns:
            Enviroment: the current selected enviroment
        """
        return self.__getattribute__(AppEnviroment.ENV_VALUE_ENV_NAME)

    def is_production_enviroment(self) -> bool:
        """Checks if the enviroment is production

        Returns
        -------
            bool: Returns if its production enviroment

        """
        return (
            self.__getattribute__(AppEnviroment.ENV_VALUE_ENV_NAME) == AppEnvironmentMode.PROD
        )

    def is_development_enviroment(self) -> bool:
        """Checks if the enviroment is development

        Returns
        -------
            bool: Returns if its development enviroment

        """
        return (
            self.__getattribute__(AppEnviroment.ENV_VALUE_ENV_NAME) == AppEnvironmentMode.DEV
        )

    def is_testing_enviroment(self) -> bool:
        """Checks if the enviroment is testing

        Returns
        -------
            bool: Returns if its testing enviroment

        """
        return (
            self.__getattribute__(AppEnviroment.ENV_VALUE_ENV_NAME) == AppEnvironmentMode.TEST
        )

    def is_log_file_provided(self) -> bool:
        """Checks if theres a valid log file provided

        Returns
        -------
            bool: Returns if theres a valid log provided

        """
        return self.__getattribute__(AppConfig.LOG_INI_FILE) is not None


PropertiesManager = _PropertiesManager()
