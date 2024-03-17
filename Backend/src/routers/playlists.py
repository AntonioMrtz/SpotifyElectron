from fastapi.responses import Response
from fastapi import APIRouter, Header, HTTPException
from typing import Optional, Union, Annotated
from model.Genre import Genre
from services.security_service import get_jwt_token
import services.playlist_service as playlist_service
import services.dto_service as dto_service
import json

router = APIRouter(
    prefix="/playlists",
    tags=["playlists"],
)


@router.get("/{nombre}", tags=["playlists"])
def get_playlist(nombre: str) -> Response:
    """ Devuelve la playlist con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre de la playlist

    Returns
    -------
        Response 200 OK

    Raises
    -------
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe una playlist con el nombre "nombre"
    """

    playlist = playlist_service.get_playlist(nombre)

    playlist_json = playlist.get_json()

    return Response(playlist_json, media_type="application/json", status_code=200)


@router.post("/", tags=["playlists"])
def post_playlist(nombre: str, foto: str, descripcion: str, nombres_canciones: list, authorization: Annotated[Union[str, None], Header()] = None) -> Response:
    """ Registra la playlist

    Parameters
    ----------
        nombre (str): Nombre de la playlist
        foto (url): url de la imagen
        descripcion (str): Descripcion de la playlist
        creador (str) : creador de la playlist
        nombres_canciones (list) : nombres de las canciones

    Returns
    -------
        Response 201 Created

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Unauthorized 401
        Not found 401
    """

    if authorization is None:
        raise HTTPException(
            status_code=401, detail="Authorization header is missing")

    jwt_token = get_jwt_token(authorization)

    result = playlist_service.create_playlist(
        name=nombre, photo=foto, description=descripcion,song_names= nombres_canciones, token=jwt_token)

    return Response(None, 201)


@router.put("/{nombre}", tags=["playlists"])
def update_playlist(nombre: str, foto: str, descripcion: str, nombres_canciones: list, nuevo_nombre: Optional[str] = None, authorization: Annotated[Union[str, None], Header()] = None) -> Response:
    """ Actualiza los parámetros de la playlist con nombre "nombre" , las canciones repetidas son serán añadidas

    Parameters
    ----------
        nombre (str): Nombre de la playlist
        nombres_canciones (list) : Lista con las canciones de la playlist
        foto (str) : url de la foto miniatura de la playlist
        nuevo_nombre (str Opcional [Valor por defecto = None]) : Nuevo nombre de la playlist, si es vacío no se actualiza
        descripcion (str) : descripción de la playlist

    Returns
    -------
        Response 204 No content

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Unauthorized 401
        Not Found 404: No existe una playlist con el nombre "nombre"
    """

    if authorization is None:
        raise HTTPException(
            status_code=401, detail="Authorization header is missing")

    jwt_token = get_jwt_token(authorization)

    playlist_service.update_playlist(
        nombre, nuevo_nombre, foto, descripcion, nombres_canciones, jwt_token)
    return Response(None, 204)


@router.delete("/{nombre}", tags=["playlists"])
def delete_playlist(nombre: str) -> Response:
    """ Elimina una playlist con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre de la playlist

    Returns
    -------
        Response 202 Accepted

    Raises
    -------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Not Found 404: No existe una playlist con el nombre "nombre"
    """

    playlist_service.delete_playlist(nombre)
    return Response(None, 202)


@router.get("/", tags=["playlists"])
def get_playlists() -> Response:
    """ Devuelve todas las playlists [ SOLO nombres canciones , no el archivo de audio ]

    Parameters
    ----------

    Returns
    -------
        Response 200 OK

    Raises
    -------
    """
    playlists = playlist_service.get_all_playlist()

    playlist_list = []
    [playlist_list.append(playlist.get_json()) for playlist in playlists]

    playlist_dict = {}

    playlist_dict["playlists"] = playlist_list
    playlist_json = json.dumps(playlist_dict)

    return Response(playlist_json, media_type="application/json", status_code=200)


@router.get("/multiple/{nombres}", tags=["playlists"])
def get_selected_playlists(nombres: str) -> Response:
    """ Devuelve todas las playlists [ SOLO nombres canciones , no el archivo de audio ]

    Parameters
    ----------

    Returns
    -------
        Response 200 OK

    Raises
    -------
    """

    playlists = playlist_service.get_selected_playlists(nombres.split(','))

    playlist_list = []
    [playlist_list.append(playlist.get_json()) for playlist in playlists]

    playlist_dict = {}

    playlist_dict["playlists"] = playlist_list
    playlist_json = json.dumps(playlist_dict)

    return Response(playlist_json, media_type="application/json", status_code=200)


# * DTO

@router.get("/dto/{nombre}")
def get_playlist_dto(nombre: str) -> Response:
    """ Devuelve la playlist con nombre "nombre" con los datos necesarios para previsualización , sin el contenido de las canciones

    Parameters
    ----------
        nombre (str): Nombre de la playlist

    Returns
    -------
        Response 200 OK

    Raises
    -------
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe una playlist con el nombre "nombre"
    """

    playlist = dto_service.get_playlist(nombre)
    playlist_json = playlist.get_json()

    return Response(playlist_json, media_type="application/json", status_code=200)
