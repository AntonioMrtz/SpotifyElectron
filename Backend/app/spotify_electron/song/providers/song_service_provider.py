"""
Provider class for supplying service depending on song architecture selected
"""

import importlib
from types import ModuleType

from app.common.app_schema import AppArchitecture, AppEnvironment
from app.common.PropertiesManager import PropertiesManager
from app.logging.logging_constants import LOGGING_SONG_SERVICE_PROVIDER
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.song.song_service_constants import SongServicePath


class SongServiceProvider:
    """Provides song service module depending on selected architecture"""

    song_service: ModuleType

    @classmethod
    def init_service(cls) -> None:
        """Init song service"""
        cls.logger = SpotifyElectronLogger(LOGGING_SONG_SERVICE_PROVIDER).get_logger()
        cls.song_services = {
            AppArchitecture.ARCH_BLOB: SongServicePath.BLOB_MODULE_NAME,
            AppArchitecture.ARCH_SERVERLESS: SongServicePath.SERVERLESS_MODULE_NAME,
        }
        cls.create_song_service()

    @classmethod
    def create_song_service(cls) -> None:
        """Creates the song service depending on the song architecture selected"""
        architecture_type = getattr(PropertiesManager, AppEnvironment.ARCHITECTURE_ENV_NAME)
        import_module = importlib.import_module(cls.song_services[architecture_type])
        cls.logger.info(f"Song service MODULE selected: {architecture_type}")
        cls.song_service = import_module

    @classmethod
    def get_song_service(cls) -> ModuleType:
        """Returns the imported song service depending on the architecture selected.

        Returns:
            ModuleType: the imported song service
        """
        return SongServiceProvider.song_service


def get_song_service() -> ModuleType:
    """Returns the song service depending on the selected architecture.
    This method could be included in SongServiceProvider as class method but\
    having a separate method ensures consistency with others providers and\
    shortens both imports and calls

    Returns:
        ModuleType: the song service module
    """
    return SongServiceProvider.get_song_service()
