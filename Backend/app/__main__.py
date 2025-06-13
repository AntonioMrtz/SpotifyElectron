"""FastAPI APP entrypoint

- Handles startup and shutdown app events
- Loads middlewares
- Creates the app object
- Configures server
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.auth_schema import AuthConfig
from app.common.app_schema import AppAuthConfig, AppConfig, AppEnvironment, AppInfo
from app.common.PropertiesManager import PropertiesManager
from app.database.DatabaseConnectionManager import DatabaseConnectionManager
from app.logging.logging_constants import LOGGING_MAIN
from app.logging.logging_schema import SpotifyElectronLogger
from app.middleware.cors_middleware_config import (
    allow_credentials,
    allowed_headers,
    allowed_methods,
    allowed_origins,
    max_age,
)
from app.spotify_electron.genre import genre_controller
from app.spotify_electron.health import health_controller
from app.spotify_electron.login import login_controller
from app.spotify_electron.playlist import playlist_controller
from app.spotify_electron.search import search_controller
from app.spotify_electron.song import song_controller
from app.spotify_electron.song.providers.song_service_provider import SongServiceProvider
from app.spotify_electron.stream import stream_controller
from app.spotify_electron.user import base_user_controller
from app.spotify_electron.user.artist import artist_controller

main_logger = SpotifyElectronLogger(LOGGING_MAIN).get_logger()


@asynccontextmanager
async def lifespan_handler(app: FastAPI) -> AsyncGenerator[None, Any]:
    """Handles the startup and shutdown events of the API

    Args:
        app: FastAPI entrypoint
    """
    environment = PropertiesManager.get_environment()
    secret_key_sign = getattr(PropertiesManager, AppEnvironment.SECRET_KEY_SIGN_ENV_NAME)
    connection_uri = getattr(PropertiesManager, AppEnvironment.MONGO_URI_ENV_NAME)

    AuthConfig.init_auth_config(
        access_token_expire_minutes=AppAuthConfig.ACCESS_TOKEN_EXPIRE_MINUTES,
        secret_key_sign=secret_key_sign,
        verification_algorithm=AppAuthConfig.VERIFICATION_ALGORITHM,
        days_to_expire_cookie=AppAuthConfig.DAYS_TO_EXPIRE_COOKIE,
    )

    await DatabaseConnectionManager.init_database_connection(
        environment=environment, connection_uri=connection_uri
    )
    SongServiceProvider.init_service()

    app.include_router(playlist_controller.router)
    app.include_router(song_controller.router)
    app.include_router(genre_controller.router)
    app.include_router(base_user_controller.router)
    app.include_router(artist_controller.router)
    app.include_router(login_controller.router)
    app.include_router(search_controller.router)
    app.include_router(stream_controller.router)
    app.include_router(health_controller.router)

    main_logger.info("Spotify Electron Backend Started")
    yield
    DatabaseConnectionManager.close_database_connection()
    main_logger.info("Spotify Electron Backend Stopped")


app = FastAPI(
    title=AppInfo.TITLE,
    version=AppInfo.VERSION,
    description=AppInfo.DESCRIPTION,
    contact={
        "name": AppInfo.CONTACT_NAME,
        "url": AppInfo.CONTACT_URL,
        "email": AppInfo.CONTACT_EMAIL,
    },
    license_info={
        "name": AppInfo.LICENSE_INFO_NAME,
        "url": AppInfo.LICENSE_INFO_URL,
    },
    lifespan=lifespan_handler,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allow_credentials,
    allow_methods=allowed_methods,
    max_age=max_age,
    allow_headers=allowed_headers,
)

if __name__ == "__main__":
    properties_manager = PropertiesManager

    is_production = properties_manager.is_production_environment()
    is_development = properties_manager.is_development_environment()

    app_path = getattr(properties_manager, AppConfig.APP_INI_KEY)
    host_ip = getattr(properties_manager, AppConfig.HOST_INI_KEY)
    host_port = int(getattr(properties_manager, AppConfig.PORT_INI_KEY))
    # force 1 worker if not production mode
    workers = int(getattr(properties_manager, AppConfig.WORKERS)) if is_production else 1

    uvicorn.run(
        app=app_path,
        host=host_ip,
        port=host_port,
        reload=is_development,
        workers=workers,
    )
