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


class _PropertiesManager:
    def __init__(self) -> None:
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
        current_directory = os.getcwd()
        self.config_file = os.path.join(
            current_directory, APP_FOLDER, RESOURCES_FOLDER, CONFIG_FILENAME
        )
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self._set_app_attributes()

    def _set_app_attributes(self):
        for key, value in self.config.items(APP_CONFIG_SECTION):
            setattr(self, key, value)

    def _load_architecture(self):
        # TODO
        architecture_type = os.getenv(ARCHITECTURE_ENV_NAME, DEFAULT_ARCHITECTURE)
        if not architecture_type:
            # TODO convert to log
            architecture_type = DEFAULT_ARCHITECTURE
            self.__setattr__(ARCHITECTURE_ENV_NAME, DEFAULT_ARCHITECTURE)
            print(f"No architecture type selected, using {DEFAULT_ARCHITECTURE}")
        self.__setattr__(ARCHITECTURE_ENV_NAME, architecture_type)
        # TODO convert to log
        print(f"Architecture selected : {architecture_type}")
        # TODO
        print(f"Running init method for architecture : {architecture_type}")

    def _load_env_variables(self, env_names: List[str]):
        # TODO
        for env_name in env_names:
            env_variable_value = os.getenv(env_name)
            if not env_variable_value:
                # TODO convert to log
                print(f"No enviroment variable provided for {env_name}")
                continue
            self.__setattr__(env_name, env_variable_value)

    def is_production_enviroment(self) -> bool:
        return self.__getattribute__(ENV_VALUE_ENV_NAME) == PROD

    def is_testing_enviroment(self) -> bool:
        return self.__getattribute__(ENV_VALUE_ENV_NAME) == TEST


PropertiesManager = _PropertiesManager()
