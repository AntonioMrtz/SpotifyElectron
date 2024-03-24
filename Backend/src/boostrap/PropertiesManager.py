import os
from typing import List

from dotenv import load_dotenv
from src.constants.set_up_constants import (
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
