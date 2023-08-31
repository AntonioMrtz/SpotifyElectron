from fastapi.responses import Response
from fastapi import APIRouter
import services.user_service as user_service
import json

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
)


@router.get("/{nombre}", tags=["usuarios"])
def get_user(nombre: str) -> Response:
    """ Devuelve el usuario con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre del usuario

    Returns
    -------
        Response 200 OK

    Raises
    -------
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe un usuario con el nombre "nombre"
    """

    usuario = user_service.get_user(nombre)

    usuario_json = usuario.get_json()

    return Response(usuario_json, media_type="application/json", status_code=200)


@router.post("/", tags=["usuarios"])
def post_usuario(nombre: str, foto: str, password: str) -> Response:
    """ Registra el usuario

    Parameters
    ----------
        nombre (str): Nombre del usuario
        foto (url): Foto de perfil del usuario
        password (str) : Contraseña del usuario

    Returns
    -------
        Response 201 Created

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
    """

    result = user_service.create_user(
        nombre, foto, password)
    return Response(None, 201)


@router.put("/{nombre}", tags=["usuarios"])
def update_playlist(nombre: str, foto: str, historial_canciones: list, playlists: list,  playlists_guardadas: list) -> Response:
    """ Actualiza los parámetros de la playlist con nombre "nombre" , las canciones repetidas son serán añadidas

    Parameters
    ----------
        nombre (str): Nombre del usuario
        foto (str) : url de la foto miniatura del usuario
        historial_canciones (list) : 5 últimas canciones reproducidas por el usuario
        playlists (list) : playlists creadas por el usuario
        playlists_guardadas (list) : playlists de otros usuarios guardadas por el usuario con nombre "nombre"

    Returns
    -------
        Response 204 No content

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Not Found 404: No existe un usuario con el nombre "nombre"
    """

    user_service.update_user(
        nombre, foto, historial_canciones, playlists, playlists_guardadas)
    return Response(None, 204)


@router.delete("/{nombre}", tags=["usuarios"])
def delete_usuario(nombre: str) -> Response:
    """ Elimina una usuario con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre del usuario

    Returns
    -------
        Response 202 Accepted

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Not Found 404: No existe un usuario con el nombre "nombre"
    """

    user_service.delete_user(nombre)
    return Response(None, 202)
