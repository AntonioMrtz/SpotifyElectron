import os
from unittest.mock import Mock

from app.common.PropertiesManager import _PropertiesManager
from app.common.set_up_constants import (
    ARCH_STREAMING_SDK,
    ARCHITECTURE_ENV_NAME,
    DEFAULT_ARCHITECTURE,
    DEV,
    DISTRIBUTION_ID_ENV_NAME,
    ENV_VALUE_ENV_NAME,
    LAMBDA_URL_ENV_NAME,
    MONGO_URI_ENV_NAME,
    PROD,
    SECRET_KEY_SIGN_ENV_NAME,
    TEST,
)

env_variables_mapping = {
    ARCHITECTURE_ENV_NAME: "ARCH",
    SECRET_KEY_SIGN_ENV_NAME: "SECRET_KEY_SIGN",
    MONGO_URI_ENV_NAME: "MONGO_URI",
    DISTRIBUTION_ID_ENV_NAME: "DISTRIBUTION_ID",
    LAMBDA_URL_ENV_NAME: "LAMBDA_URL",
    ENV_VALUE_ENV_NAME: "ENV_VALUE",
}


def test_load_env_variables(clean_modified_environments):
    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    for env_name, value in env_variables_mapping.items():
        assert properties_manager.__getattribute__(env_name) == value


def test_check_is_development_enviroment(clean_modified_environments):
    env_variables_mapping = {
        ENV_VALUE_ENV_NAME: DEV,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert properties_manager.is_development_enviroment()


def test_check_is_testing_enviroment(clean_modified_environments):
    env_variables_mapping = {
        ENV_VALUE_ENV_NAME: TEST,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert properties_manager.is_testing_enviroment()


def test_check_is_not_testing_enviroment(clean_modified_environments):
    env_variables_mapping = {
        ENV_VALUE_ENV_NAME: PROD,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert not properties_manager.is_development_enviroment()


def test_check_is_production_enviroment(clean_modified_environments):
    env_variables_mapping = {
        ENV_VALUE_ENV_NAME: PROD,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert properties_manager.is_production_enviroment()


def test_check_is_not_production_enviroment(clean_modified_environments):
    env_variables_mapping = {
        ENV_VALUE_ENV_NAME: DEV,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert not properties_manager.is_production_enviroment()


def test_load_architecture(clean_modified_environments):
    env_variables_mapping = {
        ARCHITECTURE_ENV_NAME: ARCH_STREAMING_SDK,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()
    properties_manager.__setattr__ = Mock()
    properties_manager._load_architecture()

    assert properties_manager.__setattr__.call_args[0] == (
        ARCHITECTURE_ENV_NAME,
        ARCH_STREAMING_SDK,
    )


def test_load_architecture_no_architecture_selected(clean_modified_environments):
    properties_manager = _PropertiesManager()
    arch_env_value = os.environ[ARCHITECTURE_ENV_NAME]
    if arch_env_value:
        del os.environ[ARCHITECTURE_ENV_NAME]
    properties_manager.__setattr__ = Mock()
    properties_manager._load_architecture()

    assert properties_manager.__setattr__.call_args[0] == (
        ARCHITECTURE_ENV_NAME,
        DEFAULT_ARCHITECTURE,
    )
