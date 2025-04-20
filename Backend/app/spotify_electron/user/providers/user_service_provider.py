"""User service provider"""

from typing import Annotated, Any

import app.spotify_electron.user.artist.artist_service as artist_service
import app.spotify_electron.user.base_user_service as base_user_service
import app.spotify_electron.user.user.user_service as user_service
from app.logging.logging_constants import LOGGING_USER_SERVICE_PROVIDER
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.user.user.user_schema import (
    UserType,
)

services_map = {
    UserType.USER: user_service,
    UserType.ARTIST: artist_service,
}

users_service_provider_logger = SpotifyElectronLogger(
    LOGGING_USER_SERVICE_PROVIDER
).get_logger()


async def get_user_service(user_name: str) -> Annotated[Any, "ModuleType"]:
    """Returns the user service according to the user role

    Returns:
        the user service
    """
    user_type = await base_user_service.get_user_type(user_name)
    if user_type not in services_map:
        users_service_provider_logger.warning(
            f"User {user_name} doesn't have a valid user type "
            f"using {UserType.USER} type instead"
        )
        return services_map[UserType.USER]
    return services_map[user_type]
