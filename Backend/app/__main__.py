"""
FastAPI APP entrypoint

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

from app.common.app_schema import AppConfig, AppEnvironment, AppInfo
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
from app.sentry.sentry import init_sentry
from app.spotify_electron.genre import genre_controller
from app.spotify_electron.health import health_controller
from app.spotify_electron.login import login_controller
from app.spotify_electron.playlist import playlist_controller
from app.spotify_electron.search import search_controller
from app.spotify_electron.song import song_controller
from app.spotify_electron.song.providers.song_service_provider import SongServiceProvider
from app.spotify_electron.stream import stream_controller
from app.spotify_electron.user import user_controller
from app.spotify_electron.user.artist import artist_controller

main_logger = SpotifyElectronLogger(LOGGING_MAIN).getLogger()


@asynccontextmanager
async def lifespan_handler(app: FastAPI) -> AsyncGenerator[None, Any]:
    """FastAPI the configured app object

    Args:
        app (FastAPI): Handles the the startup and shutdown events of the app
    """
    main_logger.info("Spotify Electron Backend Started")

    environment = PropertiesManager.get_environment()

    sentry_dns = getattr(PropertiesManager, AppEnvironment.SENTRY_DSN_ENV_NAME)
    init_sentry(environment, sentry_dns)

    connection_uri = getattr(PropertiesManager, AppEnvironment.MONGO_URI_ENV_NAME)
    DatabaseConnectionManager.init_database_connection(
        environment=environment, connection_uri=connection_uri
    )

    SongServiceProvider.init_service()

    app.include_router(playlist_controller.router)
    app.include_router(song_controller.router)
    app.include_router(genre_controller.router)
    app.include_router(user_controller.router)
    app.include_router(artist_controller.router)
    app.include_router(login_controller.router)
    app.include_router(search_controller.router)
    app.include_router(stream_controller.router)
    app.include_router(health_controller.router)
    yield
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
    uvicorn.run(
        app=PropertiesManager.__getattribute__(AppConfig.APP_INI_KEY),
        host=PropertiesManager.__getattribute__(AppConfig.HOST_INI_KEY),
        port=int(PropertiesManager.__getattribute__(AppConfig.PORT_INI_KEY)),
        reload=PropertiesManager.is_development_environment(),
        workers=int(PropertiesManager.__getattribute__(AppConfig.WORKERS)),
    )
