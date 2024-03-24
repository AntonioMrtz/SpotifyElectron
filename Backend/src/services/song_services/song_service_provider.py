import importlib
from types import ModuleType

from src.boostrap.PropertiesManager import PropertiesManager
from src.constants.set_up_constants import (
    ARCH_DB_BLOB,
    ARCH_STREAMING_LAMBDA,
    ARCH_STREAMING_SDK,
    ARCHITECTURE_ENV_NAME,
)
from src.constants.song_service_set_up_constants import (
    MODULE_PREFIX_NAME,
    SONG_SERVICE_DB_BLOB_SERVICE_MODULE_NAME,
    SONG_SERVICE_STREAMING_LAMBDA_SERVICE_MODULE_NAME,
    SONG_SERVICE_STREAMING_SDK_SERVICE_MODULE_NAME,
)

song_services = {
    ARCH_STREAMING_LAMBDA: SONG_SERVICE_STREAMING_LAMBDA_SERVICE_MODULE_NAME,
    ARCH_STREAMING_SDK: SONG_SERVICE_STREAMING_SDK_SERVICE_MODULE_NAME,
    ARCH_DB_BLOB: SONG_SERVICE_DB_BLOB_SERVICE_MODULE_NAME,
}


def get_song_service() -> ModuleType:
    # TODO
    song_service = importlib.import_module(
        MODULE_PREFIX_NAME
        + song_services[getattr(PropertiesManager, ARCHITECTURE_ENV_NAME)]
    )
    return song_service
