import os
from unittest.mock import Mock

from app.common.app_schema import AppArchitecture, AppEnviroment, AppEnvironmentMode
from app.common.PropertiesManager import _PropertiesManager

env_variables_mapping = {
    AppEnviroment.ARCHITECTURE_ENV_NAME: "ARCH",
    AppEnviroment.SECRET_KEY_SIGN_ENV_NAME: "SECRET_KEY_SIGN",
    AppEnviroment.MONGO_URI_ENV_NAME: "MONGO_URI",
    AppEnviroment.SERVERLESS_FUNCTION_URL_ENV_NAME: "SERVERLESS_FUNCTION_URL",
    AppEnviroment.ENV_VALUE_ENV_NAME: "ENV_VALUE",
}


def test_load_env_variables(clean_modified_environments):
    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    for env_name, value in env_variables_mapping.items():
        assert properties_manager.__getattribute__(env_name) == value


def test_check_is_development_enviroment(clean_modified_environments):
    env_variables_mapping = {
        AppEnviroment.ENV_VALUE_ENV_NAME: AppEnvironmentMode.DEV,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert properties_manager.is_development_enviroment()


def test_check_is_testing_enviroment(clean_modified_environments):
    env_variables_mapping = {
        AppEnviroment.ENV_VALUE_ENV_NAME: AppEnvironmentMode.TEST,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert properties_manager.is_testing_enviroment()


def test_check_is_not_testing_enviroment(clean_modified_environments):
    env_variables_mapping = {
        AppEnviroment.ENV_VALUE_ENV_NAME: AppEnvironmentMode.PROD,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert not properties_manager.is_development_enviroment()


def test_check_is_production_enviroment(clean_modified_environments):
    env_variables_mapping = {
        AppEnviroment.ENV_VALUE_ENV_NAME: AppEnvironmentMode.PROD,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert properties_manager.is_production_enviroment()


def test_check_is_not_production_enviroment(clean_modified_environments):
    env_variables_mapping = {
        AppEnviroment.ENV_VALUE_ENV_NAME: AppEnvironmentMode.DEV,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert not properties_manager.is_production_enviroment()


def test_load_architecture(clean_modified_environments):
    env_variables_mapping = {
        AppEnviroment.ARCHITECTURE_ENV_NAME: AppArchitecture.ARCH_STREAMING_SERVERLESS_FUNCTION,  # noqa: E501
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()
    properties_manager.__setattr__ = Mock()
    properties_manager._load_architecture()

    assert properties_manager.__setattr__.call_args[0] == (
        AppEnviroment.ARCHITECTURE_ENV_NAME,
        AppArchitecture.ARCH_STREAMING_SERVERLESS_FUNCTION,
    )


def test_load_architecture_no_architecture_selected(clean_modified_environments):
    properties_manager = _PropertiesManager()
    arch_env_value = os.environ[AppEnviroment.ARCHITECTURE_ENV_NAME]
    if arch_env_value:
        del os.environ[AppEnviroment.ARCHITECTURE_ENV_NAME]
    properties_manager.__setattr__ = Mock()
    properties_manager._load_architecture()

    assert properties_manager.__setattr__.call_args[0] == (
        AppEnviroment.ARCHITECTURE_ENV_NAME,
        AppEnviroment.DEFAULT_ARCHITECTURE,
    )
