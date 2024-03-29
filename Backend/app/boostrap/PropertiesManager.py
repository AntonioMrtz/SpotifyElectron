import configparser
import os
from typing import List

from app.constants.config_constants import (
    APP_CONFIG_SECTION,
    APP_FOLDER,
    CONFIG_FILENAME,
    RESOURCES_FOLDER,
)
from app.constants.set_up_constants import (
    ARCHITECTURE_ENV_NAME,
    DEFAULT_ARCHITECTURE,
    DISTRIBUTION_ID_ENV_NAME,
    ENV_VALUE_ENV_NAME,
    LAMBDA_URL_ENV_NAME,
    MONGO_URI_ENV_NAME,
    PROD,
    SECRET_KEY_SIGN_ENV_NAME,
    TEST,
)
from dotenv import load_dotenv

from app.logging.logger_constants import LOGGING_PROPERTIES_MANAGER
from app.logging.logging_schema import SpotifyElectronLogger

properties_manager_logger = SpotifyElectronLogger(
    LOGGING_PROPERTIES_MANAGER
).getLogger()


class _PropertiesManager:
    """Parses and stores enviroment and config files"""

    def __init__(self) -> None:
        properties_manager_logger.info("Initializing PropertiesManager")
        load_dotenv()
        self.env_variables = [
            MONGO_URI_ENV_NAME,
            SECRET_KEY_SIGN_ENV_NAME,
            DISTRIBUTION_ID_ENV_NAME,
            LAMBDA_URL_ENV_NAME,
            ENV_VALUE_ENV_NAME,
        ]
        self._load_env_variables(self.env_variables)
        self._load_architecture()
        self._load_app_config()

    def _load_app_config(self):
        """Loads app attributes from .ini file and stores them as class attributes"""
        current_directory = os.getcwd()
        self.config_file = os.path.join(
            current_directory, APP_FOLDER, RESOURCES_FOLDER, CONFIG_FILENAME
        )
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self._set_app_attributes()

    def _set_app_attributes(self):
        """Sets app atributes from .ini file into class attributes"""
        for key, value in self.config.items(APP_CONFIG_SECTION):
            setattr(self, key, value)

    def _load_architecture(self):
        """Loads the current architecture from enviroment and stores it as an\
        attribute, if none is provided DEFAULT_ARCHITECTURE will be selected"""
        architecture_type = os.getenv(ARCHITECTURE_ENV_NAME, DEFAULT_ARCHITECTURE)
        if not architecture_type:
            architecture_type = DEFAULT_ARCHITECTURE
            self.__setattr__(ARCHITECTURE_ENV_NAME, DEFAULT_ARCHITECTURE)
            properties_manager_logger.info(
                f"No architecture type selected, using {DEFAULT_ARCHITECTURE}"
            )
        self.__setattr__(ARCHITECTURE_ENV_NAME, architecture_type)
        properties_manager_logger.info(f"Architecture selected : {architecture_type}")
        properties_manager_logger.info(
            f"Running init method for architecture : {architecture_type}"
        )

    def _load_env_variables(self, env_names: List[str]):
        """Load enviroment variables into class attributes

        Args:
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

    def is_production_enviroment(self) -> bool:
        return self.__getattribute__(ENV_VALUE_ENV_NAME) == PROD

    def is_testing_enviroment(self) -> bool:
        return self.__getattribute__(ENV_VALUE_ENV_NAME) == TEST


PropertiesManager = _PropertiesManager()
