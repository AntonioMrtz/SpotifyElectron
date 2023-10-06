from fastapi.responses import Response
from fastapi import APIRouter, Header, HTTPException
from typing import Optional, Union, Annotated
from services.security_service import get_jwt_token
import services.artist_service as artist_service
import json

router = APIRouter(
    prefix="/artistas",
    tags=["artistas"],
)


@router.get("/{nombre}", tags=["artistas"])
def get_artista(nombre: str) -> Response:
    """ Devuelve el artista con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre del artista

    Returns
    -------
        Response 200 OK

    Raises
    -------
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe un artista con el nombre "nombre"
    """

    artista = artist_service.get_artist(nombre)

    artista_json = artista.get_json()

    return Response(artista_json, media_type="application/json", status_code=200)


@router.post("/", tags=["artistas"])
def post_artista(nombre: str, foto: str, password: str) -> Response:
    """ Registra el artista

    Parameters
    ----------
        nombre (str): Nombre del artista
        foto (url): Foto de perfil del artista
        password (str) : Contraseña del artista

    Returns
    -------
        Response 201 Created

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
    """

    result = artist_service.create_artist(
        nombre, foto, password)
    return Response(None, 201)


@router.put("/{nombre}", tags=["artistas"])
def update_artista(nombre: str, foto: str, historial_canciones: list, playlists: list,  playlists_guardadas: list, canciones_creadas: list, authorization: Annotated[Union[str, None], Header()] = None) -> Response:
    """ Actualiza los parámetros del artista con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre del artista
        foto (str) : url de la foto miniatura del artista
        historial_canciones (list) : 5 últimas canciones reproducidas por el artista
        playlists (list) : playlists creadas por el artista
        playlists_guardadas (list) : playlists de otros artistas guardadas por el artista con nombre "nombre"
        canciones_creadas (list) : canciones creadas por el artista

    Returns
    -------
        Response 204 No content

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        401
        Not Found 404: No existe un artista con el nombre "nombre"
    """

    if authorization is None:
        raise HTTPException(
            status_code=401, detail="Authorization header is missing")

    jwt_token = get_jwt_token(authorization)

    artist_service.update_artist(
        name=nombre, photo=foto, playback_history=historial_canciones, playlists=playlists, saved_playlists=playlists_guardadas, uploaded_songs=canciones_creadas, token=jwt_token)
    return Response(None, 204)


@router.delete("/{nombre}", tags=["artistas"])
def delete_artista(nombre: str) -> Response:
    """ Elimina un artista con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre del artista

    Returns
    -------
        Response 202 Accepted

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Not Found 404: No existe un artista con el nombre "nombre"
    """

    artist_service.delete_artist(nombre)
    return Response(None, 202)


@router.get("/", tags=["artistas"])
def get_artistas() -> Response:
    """ Devuelve todos los artistas

    Parameters
    ----------

    Returns
    -------
        Response 200 OK

    Raises
    -------
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe un artista con el nombre "nombre"
    """

    artists = artist_service.get_all_artists()

    artists_list = []
    [artists_list.append(artist.get_json()) for artist in artists]

    artists_dict = {}

    artists_dict["artists"] = artists_list
    artist_json = json.dumps(artists_dict)

    return Response(artist_json, media_type="application/json", status_code=200)


@router.get("/{nombre}/reproducciones", tags=["artistas"])
def get_reproducciones_artista(nombre: str) -> Response:
    """
    Devuelve el número de reproducciones totales de las canciones del artista

    Parameters
    ----------

    Returns
    -------
        Response 200 OK

    Raises
    -------
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe un artista con el nombre "nombre"
    """

    play_count = artist_service.get_play_count_artist(user_name=nombre)

    play_count_dict = {"play_count": play_count}

    play_count_json = json.dumps(play_count_dict)

    return Response(play_count_json, media_type="application/json", status_code=200)
