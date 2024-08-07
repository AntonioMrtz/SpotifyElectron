"""
App config schema
"""


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
