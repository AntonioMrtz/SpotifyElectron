import importlib
from types import ModuleType

from app.common.PropertiesManager import PropertiesManager
from app.constants.set_up_constants import (
    ARCH_DB_BLOB,
    ARCH_STREAMING_LAMBDA,
    ARCH_STREAMING_SDK,
    ARCHITECTURE_ENV_NAME,
)
from app.constants.song_service_set_up_constants import (
    MODULE_PREFIX_NAME,
    SONG_SERVICE_DB_BLOB_SERVICE_MODULE_NAME,
    SONG_SERVICE_STREAMING_LAMBDA_SERVICE_MODULE_NAME,
    SONG_SERVICE_STREAMING_SDK_SERVICE_MODULE_NAME,
)
from app.logging.logging_constants import LOGGING_SONG_SERVICE_PROVIDER
from app.logging.logging_schema import SpotifyElectronLogger

song_services = {
    ARCH_STREAMING_LAMBDA: SONG_SERVICE_STREAMING_LAMBDA_SERVICE_MODULE_NAME,
    ARCH_STREAMING_SDK: SONG_SERVICE_STREAMING_SDK_SERVICE_MODULE_NAME,
    ARCH_DB_BLOB: SONG_SERVICE_DB_BLOB_SERVICE_MODULE_NAME,
}

song_service_provider_logger = SpotifyElectronLogger(
    LOGGING_SONG_SERVICE_PROVIDER
).getLogger()


def get_song_service() -> ModuleType:
    # TODO
    import_module = importlib.import_module(
        MODULE_PREFIX_NAME
        + song_services[getattr(PropertiesManager, ARCHITECTURE_ENV_NAME)]
    )
    song_service_provider_logger.info(
        f"Song service MODULE selected : {song_services[getattr(PropertiesManager, ARCHITECTURE_ENV_NAME)]}"
    )
    return import_module
