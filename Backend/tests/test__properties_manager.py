import os

from app.common.app_schema import AppArchitecture, AppEnvironment, AppEnvironmentMode
from app.common.PropertiesManager import _PropertiesManager

env_variables_mapping = {
    AppEnvironment.ARCHITECTURE_ENV_NAME: "ARCH",
    AppEnvironment.SECRET_KEY_SIGN_ENV_NAME: "SECRET_KEY_SIGN",
    AppEnvironment.MONGO_URI_ENV_NAME: "MONGO_URI",
    AppEnvironment.SERVERLESS_URL_ENV_NAME: "SERVERLESS_FUNCTION_URL",
    AppEnvironment.ENV_VALUE_ENV_NAME: "ENV_VALUE",
}


def test_load_env_variables(clean_modified_environments):
    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    for env_name, value in env_variables_mapping.items():
        assert getattr(properties_manager, env_name) == value


def test_check_is_development_environment(clean_modified_environments):
    env_variables_mapping = {
        AppEnvironment.ENV_VALUE_ENV_NAME: AppEnvironmentMode.DEV,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert properties_manager.is_development_environment()


def test_check_is_testing_environment(clean_modified_environments):
    env_variables_mapping = {
        AppEnvironment.ENV_VALUE_ENV_NAME: AppEnvironmentMode.TEST,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert properties_manager.is_testing_environment()


def test_check_is_not_testing_environment(clean_modified_environments):
    env_variables_mapping = {
        AppEnvironment.ENV_VALUE_ENV_NAME: AppEnvironmentMode.PROD,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert not properties_manager.is_development_environment()


def test_check_is_production_environment(clean_modified_environments):
    env_variables_mapping = {
        AppEnvironment.ENV_VALUE_ENV_NAME: AppEnvironmentMode.PROD,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert properties_manager.is_production_environment()


def test_check_is_not_production_environment(clean_modified_environments):
    env_variables_mapping = {
        AppEnvironment.ENV_VALUE_ENV_NAME: AppEnvironmentMode.DEV,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()

    assert not properties_manager.is_production_environment()


def test_load_architecture(clean_modified_environments):
    env_variables_mapping = {
        AppEnvironment.ARCHITECTURE_ENV_NAME: AppArchitecture.ARCH_BLOB,
    }

    for env_name, value in env_variables_mapping.items():
        os.environ[env_name] = value

    properties_manager = _PropertiesManager()
    properties_manager._load_architecture()

    assert (
        getattr(properties_manager, AppEnvironment.ARCHITECTURE_ENV_NAME)
        == AppArchitecture.ARCH_BLOB
    )


def test_load_architecture_no_architecture_selected(clean_modified_environments):
    properties_manager = _PropertiesManager()
    arch_env_value = os.environ[AppEnvironment.ARCHITECTURE_ENV_NAME]
    if arch_env_value:
        del os.environ[AppEnvironment.ARCHITECTURE_ENV_NAME]
    properties_manager._load_architecture()

    assert (
        getattr(properties_manager, AppEnvironment.ARCHITECTURE_ENV_NAME)
        == AppEnvironment.DEFAULT_ARCHITECTURE
    )
