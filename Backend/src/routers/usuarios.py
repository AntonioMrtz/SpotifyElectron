import services.user_service as user_service
import services.all_users_service as all_users_service
import services.security_service as security_service
from fastapi.responses import Response
from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Union
from services.security_service import get_jwt_token
import json

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
)


@router.get("/whoami", tags=["usuarios"])
def get_whoAmI(authorization: Annotated[Union[str, None], Header()] = None) -> Response:
    """ Devuelve la información del token jwt del usuario

        Parameters
        ----------

        Returns
        -------
            Response 200 OK | TokenData as Json

        Raises
        -------
            Bad Request 400: "nombre" es vacío o nulo
            Unauthorized 401
            Not Found 404: No existe un usuario con el nombre "nombre"
        """

    if authorization is None:
        raise HTTPException(
            status_code=401, detail="Authorization header is missing")

    jwt_token = security_service.get_jwt_token(authorization)

    jwt_token_json = jwt_token.get_json()

    return Response(jwt_token_json, media_type="application/json", status_code=200)


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
def update_usuario(nombre: str, foto: str, historial_canciones: list, playlists: list,  playlists_guardadas: list, authorization: Annotated[Union[str, None], Header()] = None) -> Response:
    """ Actualiza los parámetros del usuario con nombre "nombre"

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
        Unauthorized 401
        Not Found 404: No existe un usuario con el nombre "nombre"
    """

    if authorization is None:
        raise HTTPException(
            status_code=401, detail="Authorization header is missing")

    jwt_token = get_jwt_token(authorization)

    user_service.update_user(name=nombre, photo=foto, playback_history=historial_canciones,
                             playlists=playlists, saved_playlists=playlists_guardadas, token=jwt_token)
    return Response(None, 204)


@router.delete("/{nombre}", tags=["usuarios"])
def delete_usuario(nombre: str) -> Response:
    """ Elimina un usuario con nombre "nombre"

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


@router.patch("/{nombre}/historial", tags=["usuarios"])
def patch_historial(nombre: str, nombre_cancion: str, authorization: Annotated[Union[str, None], Header()] = None) -> Response:
    """ Actualiza el historial de canciones del usuario

    Parameters
    ----------
        nombre (str): Nombre del usuario
        song_name (str): Nombre de la canción


    Returns
    -------

        Response 204
    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Unauthorized 401
        Not Found 404: No existe un usuario con el nombre "nombre" | No existe una canción con el nombre "nombre_cancion"
    """

    if authorization is None:
        raise HTTPException(
            status_code=401, detail="Authorization header is missing")

    jwt_token = get_jwt_token(authorization)

    all_users_service.add_playback_history(
        user_name=nombre, song=nombre_cancion, token=jwt_token)

    return Response(None, 204)


@router.patch("/{nombre}/playlists_guardadas", tags=["usuarios"])
def patch_playlists_guardadas(nombre: str, nombre_playlist: str, authorization: Annotated[Union[str, None], Header()] = None) -> Response:
    """ Actualiza las listas guardadas del usuario

    Parameters
    ----------
        nombre (str): Nombre del usuario
        nombre_playlist (str): Nombre de la playlist

    Returns
    -------

        Response 204

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Unauthorized 401
        Not Found 404: No existe un usuario con el nombre "nombre" | No existe una playlist con el nombre "nombre_playlist"
    """

    if authorization is None:
        raise HTTPException(
            status_code=401, detail="Authorization header is missing")

    jwt_token = get_jwt_token(authorization)

    all_users_service.add_saved_playlist(
        nombre, nombre_playlist, token=jwt_token)
    return Response(None, 204)


@router.delete("/{nombre}/playlists_guardadas", tags=["usuarios"])
def delete_playlists_guardadas(nombre: str, nombre_playlist: str, authorization: Annotated[Union[str, None], Header()] = None) -> Response:
    """ Elimina la playlist de las playlist guardadas del usuario

    Parameters
    ----------
        nombre (str): Nombre del usuario
        nombre_playlist (str): Nombre de la playlist

    Returns
    -------

        Response 202

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Unauthorized 401
        Not Found 404: No existe un usuario con el nombre "nombre" | No existe una playlist con el nombre "nombre_playlist"
    """

    if authorization is None:
        raise HTTPException(
            status_code=401, detail="Authorization header is missing")

    jwt_token = get_jwt_token(authorization)

    all_users_service.delete_saved_playlist(
        nombre, nombre_playlist, token=jwt_token)
    return Response(None, 202)
