from fastapi import FastAPI, APIRouter, UploadFile, status, Depends, Header, HTTPException
from typing import Annotated, Union
from services.security_service import get_jwt_token
from model.Genre import Genre
from fastapi.responses import Response
from sys import modules
import services.dto_service as dto_service
import services.song_service as song_service_streaming
import json

router = APIRouter(
    prefix="/canciones",
    tags=["canciones"],
)

""" if "pytest" in modules:
    song_service = song_service_database

else: """
song_service = song_service_streaming


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
async def post_cancion(nombre: str, genero: Genre, foto: str, file: UploadFile, authorization: Annotated[Union[str, None], Header()] = None) -> Response:
    """ Registra la canción con los parámetros "nombre","artista" y "género"

    Parameters
    ----------
        nombre (str): Nombre de la canción
        genero (Genre): Género musical de la canción
        foto (url): Género musical de la canción


    Returns
    -------
        Response 201 Created

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Unauthorized 401
    """

    readFile = await file.read()

    if authorization is None:
        raise HTTPException(
            status_code=401, detail="Authorization header is missing")

    jwt_token = get_jwt_token(authorization)

    await song_service.create_song(nombre, genero, foto, readFile, jwt_token)
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


@router.delete("/{nombre}")
def delete_cancion(nombre: str) -> Response:
    """ Borra una canción a partir de "nombre"

    Parameters
    ----------
        nombre (str): Nombre de la canción

    Returns
    -------
        Response 202 Accepted

    Raises
    -------
        Bad Request 400 : Parámetros inválidos
        Not found 404: La canción con ese nombre no existe
    """

    song_service.delete_song(nombre)

    return Response(None, 202)


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


@router.put("/{nombre}")
def update_song(nombre: str, foto: str = None, genre: Genre = None, nuevo_nombre: str = None, authorization: Annotated[Union[str, None], Header()] = None) -> Response:
    """ Actualiza los parámetros de la cancion con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre de la cancion
        artist (str): Artista de la cancion
        foto (url): Foto de la cancion
        genre (Genre): Genero de la cancion
        nuevo_nombre (str): Nuevo nombre de la cancion

    Returns
    -------
        Response 204 No content

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Not Found 404: No existe una cancion con el nombre "nombre"
        Unauthorized 401
    """

    if authorization is None:
        raise HTTPException(
            status_code=401, detail="Authorization header is missing")

    jwt_token = get_jwt_token(authorization)

    song_service.update_song(
        nombre, nuevo_nombre, foto, genre, jwt_token)
    return Response(None, 204)


@router.patch("/{nombre}/numberOfPlays")
def increase_number_plays_song(nombre: str) -> Response:
    """ Incrementa el número de visitas de la cancion con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre de la cancion

    Returns
    -------
        Response 204 No content

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Not Found 404: No existe una cancion con el nombre "nombre"
    """

    song_service.increase_number_plays(nombre)
    return Response(None, 204)


@router.get("/generos/{genero}")
def get_cancion_por_genero(genero: Genre) -> Response:
    """ Obtiene todas las playlist de un género

    Parameters
    ----------
        genero (Genre): Género para filtrar

    Returns
    -------
        Response 200 OK

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Not Found 404: Género no existe
    """

    filtered_songs = dto_service.get_songs_by_genero(genero)

    filtered_songs_list = []
    [filtered_songs_list.append(song.get_json()) for song in filtered_songs]

    songs_dict = {}

    songs_dict["songs"] = filtered_songs_list
    songs_json = json.dumps(songs_dict)

    return Response(songs_json, media_type="application/json", status_code=200)
