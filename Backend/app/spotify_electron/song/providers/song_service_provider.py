"""Song service provider based on selected architecture"""

import importlib
from types import ModuleType

from app.common.app_schema import AppArchitecture, AppEnvironment
from app.common.PropertiesManager import PropertiesManager
from app.logging.logging_constants import LOGGING_SONG_SERVICE_PROVIDER
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.song.base_song_schema import SongServiceHealthCheckError
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
        cls._create_song_service()

    @classmethod
    def _create_song_service(cls) -> None:
        """Creates the song service depending on the song architecture selected"""
        architecture_type = cls._get_current_architecture()
        import_module = importlib.import_module(cls.song_services[architecture_type])
        cls.logger.info(f"Song service MODULE selected: {architecture_type}")
        cls.song_service = import_module

    @classmethod
    def get_song_service(cls) -> ModuleType:
        """Returns the imported song service depending on the architecture selected.

        Returns:
            the imported song service
        """
        return SongServiceProvider.song_service

    @classmethod
    def check_service_health(cls) -> bool:
        """Check if the song service initialized and functioning.

        Returns:
            bool: True if the song service is operational, False otherwise

        Raises:
            SongServiceHealthCheckError: When health check fail on service provider
        """
        try:
            if not hasattr(cls, "song_service") or not cls.song_service:
                cls.logger.warning("Song service not initialized")
                return False
            method_list = [
                method
                for method in dir(cls.song_service)
                if callable(getattr(cls.song_service, method)) and not method.startswith("__")
            ]
            for method in method_list:
                if not hasattr(cls.song_service, method):
                    cls.logger.warning(f"Song servise missing required method: {method}")
        except Exception as exception:
            cls.logger.exception("Error checking song service health")
            raise SongServiceHealthCheckError from exception
        else:
            cls.logger.info("Song service health check successful")
            return True

    @classmethod
    def _get_current_architecture(cls) -> AppArchitecture:
        """Get the current architecture type."""
        return getattr(PropertiesManager, AppEnvironment.ARCHITECTURE_ENV_NAME)


def get_song_service() -> ModuleType:
    """Returns the song service depending on the selected architecture.
    This method could be included in SongServiceProvider as class method but\
    having a separate method ensures consistency with others providers and\
    shortens both imports and calls

    Returns:
        the song service module
    """
    return SongServiceProvider.get_song_service()
