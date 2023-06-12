from fastapi import FastAPI,UploadFile,status
import services.song_service as song_service
import services.list_service as list_service
from fastapi.responses import Response

from model.Genre import Genre


app = FastAPI(title="SpotifyElectronAPI",
              description="API created with FastAPI Python to serve as backend for SpotifyElectron App",
              version="0.0.1",

              )


# Devuelve todas las listas
@app.get("/listas/")
async def get_listas():

    pass

@app.get("/canciones/{nombre}")
async def get_cancion(nombre : str) -> Response:
    """ Devuelve la canción con nombre "nombre"

    Args:
        nombre (str): Nombre de la canción
        
    Returns:
        Response 200 OK: Cancion en el body de la respuesta

    Raises:
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe una canción con el nombre "nombre"


    """
    return await song_service.get_song(id)


# Devuelve todas las canciones
@app.get("/canciones/")
async def get_canciones():
    pass

# Sube una cancion
@app.post("/canciones/")
async def post_cancion(nombre : str, artista : str,genero : Genre,file : UploadFile) -> Response:
    """ Registra la canción con los parámetros "nombre","artista" y "género"

    Args:
        nombre (str): Nombre de la canción
        artista (str): Artista de la canción
        genero (Genre): Género musical de la canción
   
    Returns:
        Response 201 Created

    Raises:
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Internal Server Error?
    """
    readFile = await file.read()
    return song_service.create_song(nombre,artista,genero,readFile)

