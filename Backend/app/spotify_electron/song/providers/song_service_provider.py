"""
Provider class for supplying service depending on song architecture selected
"""

import importlib
from types import ModuleType

from app.common.app_schema import AppArchitecture, AppEnviroment
from app.common.PropertiesManager import PropertiesManager
from app.logging.logging_constants import LOGGING_SONG_SERVICE_PROVIDER
from app.logging.logging_schema import SpotifyElectronLogger
from app.patterns.Factory import BaseSongServiceModuleFactory
from app.spotify_electron.song.song_service_constants import (
    MODULE_PREFIX_NAME,
    SONG_SERVICE_BLOB_MODULE_NAME,
    SONG_SERVICE_STREAMING_AWS_SERVERLESS_FUNCTION_MODULE_NAME,
)


class SongServiceModuleFactory(BaseSongServiceModuleFactory):
    """Concrete implementation for selecting song service depeding on architecture selected"""

    def __init__(self) -> None:
        self.song_services = {
            AppArchitecture.ARCH_STREAMING_SERVERLESS_FUNCTION: SONG_SERVICE_STREAMING_AWS_SERVERLESS_FUNCTION_MODULE_NAME,  # noqa: E501
            AppArchitecture.ARCH_BLOB: SONG_SERVICE_BLOB_MODULE_NAME,
        }
        self.logger = SpotifyElectronLogger(LOGGING_SONG_SERVICE_PROVIDER).getLogger()
        super().__init__()

    def create_song_service(self) -> ModuleType:
        """Creates the song service depending on the song architecture selected

        Returns:
            ModuleType: the song module based on current architecture
        """
        return self._get_song_service()

    def _get_song_service(self) -> ModuleType:
        """Returns the imported song service depending on the architecture selected

        Returns:
            ModuleType: the imported song service
        """
        architecture_type = getattr(PropertiesManager, AppEnviroment.ARCHITECTURE_ENV_NAME)
        import_module = importlib.import_module(
            MODULE_PREFIX_NAME + self.song_services[architecture_type]
        )
        self.logger.info(f"Song service MODULE selected : {architecture_type}")
        return import_module


def get_song_service() -> ModuleType:
    """Returns the song service depending on the selected architecture

    Returns:
        ModuleType: the song service module
    """
    return SongServiceModuleFactory().create_song_service()
