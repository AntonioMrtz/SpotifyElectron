"""
App config schema
"""

from enum import StrEnum


class AppInfo:
    """App info constants"""

    TITLE = "Spotify Electron Backend API"
    DESCRIPTION = "API created with Python FastAPI to serve\
          as backend for Spotify Electron music streaming Desktop App"
    VERSION = "2.0.1"
    CONTACT_NAME = "Antonio Martínez Fernández"
    CONTACT_URL = "https://github.com/AntonioMrtz"
    CONTACT_EMAIL = "antoniomartinezfernandez17@gmail.com"
    LICENSE_INFO_NAME = "Attribution-NonCommercial-ShareAlike 4.0 International"
    LICENSE_INFO_URL = "https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es"
    SERVER = [
        {"url": "http://127.0.0.1:8000"}
    ]  # may cause CORS on local development when using swagger


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
    WORKERS = "workers"


class AppEnvironmentMode(StrEnum):
    """App environment mode constants"""

    PROD = "PROD"
    DEV = "DEV"
    TEST = "TEST"


class AppArchitecture(StrEnum):
    """App architecture constants"""

    ARCH_BLOB = "BLOB"
    ARCH_SERVERLESS = "SERVERLESS"


class AppAuthConfig:
    """App authentication configuration"""

    VERTIFICATION_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 days
    DAYS_TO_EXPIRE_COOKIE = 7


class AppEnvironment:
    """App environment constants"""

    ARCHITECTURE_ENV_NAME = "ARCH"

    DEFAULT_ARCHITECTURE = AppArchitecture.ARCH_BLOB
    MONGO_URI_ENV_NAME = "MONGO_URI"
    SERVERLESS_URL_ENV_NAME = "SERVERLESS_FUNCTION_URL"
    ENV_VALUE_ENV_NAME = "ENV_VALUE"
