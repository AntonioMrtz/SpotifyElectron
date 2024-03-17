from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware.middleware import CheckJwtAuth
from routers import artistas, canciones, generos, login, playlists, search, usuarios

app = FastAPI(
    title="SpotifyElectronAPI",
    description="API created with FastAPI Python to manage backend for \
        Spotify Electron App https://github.com/AntonioMrtz/SpotifyElectron",
    version="0.0.1",
)

""" Cors disabled """
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost/",
        "http://localhost:1212",
        "https://localhost:1212/",
        "https://localhost",
        "https://localhost:1212",
        "https://localhost:1212/",
        "http://127.0.0.1:8000/",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8000/usuarios/",
    ],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "PATCH"],
    max_age=3600,
    allow_headers=["*"],
)

app.add_middleware(CheckJwtAuth)

app.include_router(playlists.router)
app.include_router(canciones.router)
app.include_router(generos.router)
app.include_router(usuarios.router)
app.include_router(artistas.router)
app.include_router(login.router)
app.include_router(search.router)
