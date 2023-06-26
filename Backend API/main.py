from fastapi import FastAPI,UploadFile,status
import services.song_service as song_service
import services.list_service as list_service
from fastapi.responses import Response
import json
from model.Genre import Genre
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="SpotifyElectronAPI",
              description="API created with FastAPI Python to serve as backend for SpotifyElectron App",
              version="0.0.1"

              )
""" Cors disabled """
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET","PUT","DELETE"],
		allow_headers=["*"],
    max_age=3600,
)


# Devuelve todas las listas
@app.get("/listas/")
async def get_listas():

    list_service.hola()
    """ prueba = {"prueba":"prueba"}
    return Response(json.dumps(prueba) , 201) """

@app.get("/canciones/{nombre}")
def get_cancion(nombre : str) -> Response:
    """ Devuelve la canción con nombre "nombre"

    Args:
        nombre (str): Nombre de la canción
        
    Returns:
        Response 200 OK: Cancion en el body de la respuesta

    Raises:
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe una canción con el nombre "nombre"


    """
    song = song_service.get_song(nombre)

    song_json = json.dumps(song.__dict__)

    return Response(song_json, media_type="application/json", status_code=200)
    
    #return Response(song, media_type="audio/mp3", status_code=200)


# Devuelve todas las canciones
@app.get("/canciones/")
async def get_canciones():
    await song_service.get_songs()

# Sube una cancion
@app.post("/canciones/")
async def post_cancion(nombre : str, artista : str,genero : Genre,foto : str,file : UploadFile) -> Response:
    """ Registra la canción con los parámetros "nombre","artista" y "género"

    Args:
        nombre (str): Nombre de la canción
        artista (str): Artista de la canción
        genero (Genre): Género musical de la canción
        foto (url): Género musical de la canción

   
    Returns:
        Response 201 Created

    Raises:
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Internal Server Error?
    """
    readFile = await file.read()
    song_service.create_song(nombre,artista,genero,foto,readFile)
    return Response(None, 201)

