import os
from unittest.mock import Mock

from src.constants.set_up_constants import (
    ARCH_STREAMING_SDK,
    PROD,
    MONGO_URI_ENV_NAME,
    ARCHITECTURE_ENV_NAME,
    DEFAULT_ARCHITECTURE,
    DISTRIBUTION_ID_ENV_NAME,
    ENV_VALUE_ENV_NAME,
    LAMBDA_URL_ENV_NAME,
    SECRET_KEY_SIGN_ENV_NAME,
    TEST,
)
from src.boostrap.PropertiesManager import _PropertiesManager


env_variables_mapping = {
    ARCHITECTURE_ENV_NAME: "ARCH",
    SECRET_KEY_SIGN_ENV_NAME: "SECRET_KEY_SIGN",
    MONGO_URI_ENV_NAME: "MONGO_URI",
    DISTRIBUTION_ID_ENV_NAME: "DISTRIBUTION_ID",
    LAMBDA_URL_ENV_NAME: "LAMBDA_URL",
    ENV_VALUE_ENV_NAME: "ENV_VALUE",
}


def test_load_env_variables(clean_environment):

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    for env_name, value in env_variables_mapping.items():
        assert properties_manager.__getattribute__(env_name) == value


def test_check_is_testing_enviroment(clean_environment):

    env_variables_mapping = {
        ENV_VALUE_ENV_NAME: TEST,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert properties_manager.is_testing_enviroment()


def test_check_is_not_testing_enviroment(clean_environment):

    env_variables_mapping = {
        ENV_VALUE_ENV_NAME: PROD,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert not properties_manager.is_testing_enviroment()


def test_check_is_production_enviroment(clean_environment):

    env_variables_mapping = {
        ENV_VALUE_ENV_NAME: PROD,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert properties_manager.is_production_enviroment()


def test_check_is_not_production_enviroment(clean_environment):

    env_variables_mapping = {
        ENV_VALUE_ENV_NAME: TEST,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert not properties_manager.is_production_enviroment()


def test_load_architecture(clean_environment):
    env_variables_mapping = {
        ARCHITECTURE_ENV_NAME: ARCH_STREAMING_SDK,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()
    properties_manager.__setattr__ = Mock()
    load_architecture_method = getattr(
        properties_manager, "_PropertiesManager__load_architecture"
    )
    load_architecture_method()

    assert properties_manager.__setattr__.call_args[0] == (
        ARCHITECTURE_ENV_NAME,
        ARCH_STREAMING_SDK,
    )


def test_load_architecture_no_architecture_selected(clean_environment):
    properties_manager = _PropertiesManager()
    properties_manager.__setattr__ = Mock()
    load_architecture_method = getattr(
        properties_manager, "_PropertiesManager__load_architecture"
    )
    load_architecture_method()

    assert properties_manager.__setattr__.call_args[0] == (
        ARCHITECTURE_ENV_NAME,
        DEFAULT_ARCHITECTURE,
    )
