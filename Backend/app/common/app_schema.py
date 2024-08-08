"""
App config schema
"""

from enum import StrEnum


class AppInfo:
    """App info constants"""

    TITLE = "Spotify Electron Backend API"
    DESCRIPTION = "API created with Python FastAPI to serve\
          as backend for Spotify Electron music streaming Desktop App"
    VERSION = "1.0.0"
    CONTACT_NAME = "Antonio Martínez Fernández"
    CONTACT_URL = "https://github.com/AntonioMrtz"
    CONTACT_EMAIL = "antoniomartinezfernandez17@gmail.com"
    LICENSE_INFO_NAME = "Attribution-NonCommercial-ShareAlike 4.0 International"
    LICENSE_INFO_URL = "https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es"


class AppConfig:
    """App config constants"""

    # files/folders
    RESOURCE_FOLDER = "resources"
    APP_FOLDER = "app"
    CONFIG_FILENAME = "config.ini"
    # log
    LOG_INI_SECTION = "log"
    LOG_INI_FILE = "log_file"
    LOG_INI_LEVEL = "log_level"
    # app
    APP_INI_SECTION = "app"
    APP_INI_KEY = "app.path"
    HOST_INI_KEY = "host"
    PORT_INI_KEY = "port"


class AppEnvironmentMode(StrEnum):
    """App enviroment mode constants"""

    PROD = "PROD"
    DEV = "DEV"
    TEST = "TEST"


class AppArchitecture:
    """App architecture constants"""

    ARCH_STREAMING_SERVERLESS_FUNCTION = "STREAMING_SERVERLESS_FUNCTION"
    ARCH_BLOB = "BLOB"


class AppEnviroment:
    """App enviroment constants"""

    ARCHITECTURE_ENV_NAME = "ARCH"
    DEFAULT_ARCHITECTURE = AppArchitecture.ARCH_BLOB

    SECRET_KEY_SIGN_ENV_NAME = "SECRET_KEY_SIGN"
    MONGO_URI_ENV_NAME = "MONGO_URI"
    SERVERLESS_FUNCTION_URL_ENV_NAME = "SERVERLESS_FUNCTION_URL"
    ENV_VALUE_ENV_NAME = "ENV_VALUE"
