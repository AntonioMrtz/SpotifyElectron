from typing import Annotated

from fastapi import APIRouter, Body, Header
from fastapi.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED

import app.spotify_electron.security.security_service as security_service
import app.spotify_electron.user.all_users_service as all_users_service
import app.spotify_electron.user.user_service as user_service
import app.spotify_electron.utils.json_converter.json_converter_service as json_converter_service
from app.spotify_electron.security.security_schema import BadJWTTokenProvidedException

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/whoami")
def get_whoAmI(authorization: Annotated[str | None, Header()] = None) -> Response:
    """Devuelve la información del token jwt del usuario

    Parameters
    ----------

    Returns
    -------
        Response 200 OK | TokenData as Json

    Raises
    ------
        Bad Request 400: "nombre" es vacío o nulo
        Unauthorized 401
        Not Found 404: No existe un usuario con el nombre "nombre"

    """
    try:
        jwt_token = security_service.get_jwt_token_data(authorization)
        jwt_token_json = json_converter_service.get_json_from_model(jwt_token)

        return Response(jwt_token_json, media_type="application/json", status_code=200)
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/{name}")
def get_user(name: str) -> Response:
    """Devuelve el usuario con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre del usuario

    Returns
    -------
        Response 200 OK

    Raises
    ------
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe un usuario con el nombre "nombre"

    """
    usuario = all_users_service.get_user(name)
    usuario_json = json_converter_service.get_json_from_model(usuario)

    return Response(usuario_json, media_type="application/json", status_code=200)


@router.get("/{nombre}/playlists")
def get_playlists_by_user(name: str) -> Response:
    # TODO get playlists by user
    # TODO hacer test

    user = user_service.get_user(name)
    user_json = json_converter_service.get_json_from_model(user)

    return Response(user_json, media_type="application/json", status_code=200)


@router.post("/")
def post_user(name: str, photo: str, password: str) -> Response:
    """Registra el usuario

    Parameters
    ----------
        nombre (str): Nombre del usuario
        foto (url): Foto de perfil del usuario
        password (str) : Contraseña del usuario

    Returns
    -------
        Response 201 Created

    Raises
    ------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos

    """
    user_service.create_user(name, photo, password)
    return Response(None, 201)


@router.put("/{name}")
def update_user(
    name: str,
    photo: str,
    playback_history: list[str] = Body(...),
    playlists: list[str] = Body(...),
    saved_playlists: list[str] = Body(...),
    authorization: Annotated[str | None, Header()] = None,
) -> Response:
    """Actualiza los parámetros del usuario con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre del usuario
        foto (str) : url de la foto miniatura del usuario
        historial_canciones (list) : 5 últimas canciones reproducidas por el usuario
        playlists (list) : playlists creadas por el usuario
        playlists_guardadas (list) : playlists de otros usuarios guardadas por el
                                     usuario con nombre "nombre"

    Returns
    -------
        Response 204 No content

    Raises
    ------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Unauthorized 401
        Not Found 404: No existe un usuario con el nombre "nombre"

    """
    try:
        jwt_token = security_service.get_jwt_token_data(authorization)

        user_service.update_user(
            name=name,
            photo=photo,
            playback_history=playback_history,
            playlists=playlists,
            saved_playlists=saved_playlists,
            token=jwt_token,
        )
        return Response(None, 204)
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.delete("/{name}")
def delete_user(name: str) -> Response:
    """Elimina un usuario con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre del usuario

    Returns
    -------
        Response 202 Accepted

    Raises
    ------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Not Found 404: No existe un usuario con el nombre "nombre"

    """
    user_service.delete_user(name)
    return Response(None, 202)


@router.patch("/{name}/playback_history")
def patch_playback_history(
    name: str,
    song_name: str,
    authorization: Annotated[str | None, Header()] = None,
) -> Response:
    """Actualiza el historial de canciones del usuario

    Parameters
    ----------
        nombre (str): Nombre del usuario
        song_name (str): Nombre de la canción


    Returns
    -------
        Response 204

    Raises
    ------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Unauthorized 401
        Not Found 404: No existe un usuario con el nombre "nombre" |
                       No existe una canción con el nombre "nombre_cancion"

    """
    try:
        jwt_token = security_service.get_jwt_token_data(authorization)

        all_users_service.add_playback_history(
            user_name=name, song=song_name, token=jwt_token
        )

        return Response(None, 204)
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.patch("/{name}/saved_playlists")
def patch_saved_playlists(
    name: str,
    playlist_name: str,
    authorization: Annotated[str | None, Header()] = None,
) -> Response:
    """Actualiza las listas guardadas del usuario

    Parameters
    ----------
        nombre (str): Nombre del usuario
        nombre_playlist (str): Nombre de la playlist

    Returns
    -------
        Response 204

    Raises
    ------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Unauthorized 401
        Not Found 404: No existe un usuario con el nombre "nombre" |
                       No existe una playlist con el nombre "nombre_playlist"

    """
    try:
        jwt_token = security_service.get_jwt_token_data(authorization)

        all_users_service.add_saved_playlist(name, playlist_name, token=jwt_token)
        return Response(None, 204)
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.delete("/{name}/saved_playlists")
def delete_saved_playlists(
    name: str,
    playlist_name: str,
    authorization: Annotated[str | None, Header()] = None,
) -> Response:
    """Elimina la playlist de las playlist guardadas del usuario

    Parameters
    ----------
        nombre (str): Nombre del usuario
        nombre_playlist (str): Nombre de la playlist

    Returns
    -------
        Response 202

    Raises
    ------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Unauthorized 401
        Not Found 404: No existe un usuario con el nombre "nombre" |
                       No existe una playlist con el nombre "nombre_playlist"

    """
    try:
        jwt_token = security_service.get_jwt_token_data(authorization)

        all_users_service.delete_saved_playlist(name, playlist_name, token=jwt_token)
        return Response(None, 202)
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
