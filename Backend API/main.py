from fastapi import FastAPI,UploadFile,status

import services.song_service as song_service
import services.list_service as list_service


app = FastAPI(title="SpotifyElectronAPI",
              description="API created with FastAPI Python to serve as backend for SpotifyElectron App",
              version="0.0.1",

              )

# Devuelve todas las listas
@app.get("/listas/")
async def get_listas():

    pass

# Devuelve la cancion
@app.get("/canciones/{id}")
async def get_canciones(id : str):
    song_service.get_song(id)


# Devuelve todas las canciones
@app.get("/canciones/")
async def get_canciones():
    pass

# Sube una cancion
@app.post("/canciones/",status_code=status.HTTP_201_CREATED)
async def post_canciones(nombre : str, artista : str,genero : str,file : UploadFile):
    readFile = await file.read()
    return song_service.create_song(nombre,artista,genero,readFile)

