from fastapi import FastAPI, Request , Response
from fastapi.middleware.cors import CORSMiddleware
from routers import playlists, canciones, generos, usuarios, artistas , login
from services.security_service import check_jwt_is_valid
from middleware.middleware import CheckJwtAuth

""" from middleware import jwt_middleware
 """

app = FastAPI(title="SpotifyElectronAPI",
              description="API created with FastAPI Python to serve as backend for SpotifyElectron App",
              version="0.0.1"
              )

""" Cors disabled """
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:1212"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "PATCH"],
    max_age=3600,


)
"""     allow_headers=['Set-Cookie','Access-Control-Allow-Origin'], expose_headers=["Set-Cookie"],
 """

""" app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:1212"],
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "PATCH"],
    max_age=3600,
)
 """
app.add_middleware(CheckJwtAuth)


app.include_router(playlists.router)
app.include_router(canciones.router)
app.include_router(generos.router)
app.include_router(usuarios.router)
app.include_router(artistas.router)
app.include_router(login.router)

