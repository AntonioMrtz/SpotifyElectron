from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import playlists,canciones,generos

app = FastAPI(title="SpotifyElectronAPI",
              description="API created with FastAPI Python to serve as backend for SpotifyElectron App",
              version="0.0.1"

              )
""" Cors disabled """
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
  		allow_headers=["*"],
    max_age=3600,
)


app.include_router(playlists.router)
app.include_router(canciones.router)
app.include_router(generos.router)

