from fastapi.responses import Response
from fastapi import APIRouter
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
def update_artista(nombre: str, foto: str, historial_canciones: list, playlists: list,  playlists_guardadas: list, canciones_creadas: list) -> Response:
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
        Not Found 404: No existe un artista con el nombre "nombre"
    """

    artist_service.update_artist(
        name=nombre, photo=foto, playback_history=historial_canciones, playlists=playlists, saved_playlists=playlists_guardadas, uploaded_songs=canciones_creadas)
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
