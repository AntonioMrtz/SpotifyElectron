"""
FastAPI App entrypoint

- Handles startup and shutdown app events
- Load middlewares
- Creates the app object
- Configure Uvicorn server

"""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.common.config_constants import APP, HOST, PORT
from app.common.PropertiesManager import PropertiesManager
from app.database.Database import Database
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
from app.spotify_electron.user import user_controller
from app.spotify_electron.user.artist import artist_controller

main_logger = SpotifyElectronLogger(LOGGING_MAIN).getLogger()


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    """Handles the the startup and shutdown events of the app

    Parameters
    ----------
    app : FastAPI
        the app object that is going to be created

    """
    main_logger.info("Spotify Electron Backend Started")

    Database()

    app.include_router(playlist_controller.router)
    app.include_router(song_controller.router)
    app.include_router(genre_controller.router)
    app.include_router(user_controller.router)
    app.include_router(artist_controller.router)
    app.include_router(login_controller.router)
    app.include_router(search_controller.router)
    app.include_router(health_controller.router)
    yield
    main_logger.info("Spotify Electron Backend Stopped")


app = FastAPI(
    title="SpotifyElectronAPI",
    description="API created with FastAPI Python to serve \
        as backend for Spotify Electron music streaming Desktop App",
    version="1.0.0",
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
        app=PropertiesManager.__getattribute__(APP),
        host=PropertiesManager.__getattribute__(HOST),
        port=int(PropertiesManager.__getattribute__(PORT)),
        reload=PropertiesManager.is_development_enviroment(),
    )
