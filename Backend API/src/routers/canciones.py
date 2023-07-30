from fastapi import FastAPI,APIRouter, UploadFile, status
from model.Genre import Genre
from fastapi.responses import Response
import services.dto_service as dto_service
import services.song_service as song_service
import json

router = APIRouter(
    prefix="/canciones",
    tags=["canciones"],
)


@router.get("/{nombre}")
def get_cancion(nombre: str) -> Response:
    """ Devuelve la canción con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre de la canción

    Returns
    -------
        Response 200 OK

    Raises
    -------
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe una canción con el nombre "nombre"
    """

    song = song_service.get_song(nombre)
    song_json = song.get_json()

    return Response(song_json, media_type="application/json", status_code=200)


@router.post("/")
async def post_cancion(nombre: str, artista: str, genero: Genre, foto: str, file: UploadFile) -> Response:
    """ Registra la canción con los parámetros "nombre","artista" y "género"

    Parameters
    ----------
        nombre (str): Nombre de la canción
        artista (str): Artista de la canción
        genero (Genre): Género musical de la canción
        foto (url): Género musical de la canción


    Returns
    -------
        Response 201 Created

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
    """

    readFile = await file.read()
    await song_service.create_song(nombre, artista, genero, foto, readFile)
    return Response(None, 201)


@router.get("/")
def get_canciones() -> Response:
    """ Devuelve todas las canciones

    Parameters
    ----------

    Returns
    -------
        Response 200 OK

    Raises
    -------
    """

    songs = song_service.get_all_songs()

    songs_list = []
    [songs_list.append(song.get_json()) for song in songs]

    songs_dict = {}

    songs_dict["songs"] = songs_list
    songs_json = json.dumps(songs_dict)

    return Response(songs_json, media_type="application/json", status_code=200)


@router.get("/dto/{nombre}")
def get_cancion_dto(nombre: str) -> Response:
    """ Devuelve la canción con nombre "nombre" con los dato necesarios para previsualizacion sin carga el contenido de la canción

    Parameters
    ----------
        nombre (str): Nombre de la canción

    Returns
    -------
        Response 200 OK

    Raises
    -------
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe una canción con el nombre "nombre"
    """

    song = dto_service.get_song(nombre)
    song_json = song.get_json()

    return Response(song_json, media_type="application/json", status_code=200)



#TODO documentacion y pulir

@router.delete("/{nombre}")
def get_cancion_dto(nombre: str) -> Response:
    song_service.delete_song(nombre)

    return Response(None, 202)
