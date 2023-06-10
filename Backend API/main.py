from fastapi import FastAPI

import services.song_service as song_service
import services.list_service as list_service

import json

import logging

logging.basicConfig(level=logging.DEBUG)


app = FastAPI(title="SpotifyElectronAPI",
              description="API created with FastAPI Python to serve as backend for SpotifyElectron App",
              version="0.0.1",

              )

# Devuelve todas las listas
@app.get("/listas/")
def get_listas():

    song_service.prueba()
