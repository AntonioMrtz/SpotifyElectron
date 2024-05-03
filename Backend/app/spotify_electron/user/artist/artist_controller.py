import json
from typing import Annotated

from fastapi import APIRouter, Body, Header
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

import app.spotify_electron.security.security_service as security_service
import app.spotify_electron.user.artist.artist_service as artist_service
import app.spotify_electron.utils.json_converter.json_converter_service as json_converter_service
from app.spotify_electron.security.security_schema import BadJWTTokenProvidedException

router = APIRouter(
    prefix="/artistas",
    tags=["Artists"],
)


@router.get("/{nombre}", tags=["artistas"])
def get_artista(nombre: str) -> Response:
    """Devuelve el artista con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre del artista

    Returns
    -------
        Response HTTP_200_OK OK

    Raises
    ------
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe un artista con el nombre "nombre"

    """
    artista = artist_service.get_artist(nombre)
    artista_json = json_converter_service.get_json_from_model(artista)

    return Response(
        artista_json, media_type="application/json", status_code=HTTP_200_OK
    )


@router.post("/", tags=["artistas"])
def post_artista(nombre: str, foto: str, password: str) -> Response:
    """Registra el artista

    Parameters
    ----------
        nombre (str): Nombre del artista
        foto (url): Foto de perfil del artista
        password (str) : Contraseña del artista

    Returns
    -------
        Response 201 Created

    Raises
    ------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos

    """
    artist_service.create_artist(nombre, foto, password)
    return Response(None, 201)


@router.put("/{nombre}", tags=["artistas"])
def update_artista(
    nombre: str,
    foto: str,
    historial_canciones: list[str] = Body(...),
    playlists: list[str] = Body(...),
    playlists_guardadas: list[str] = Body(...),
    canciones_creadas: list[str] = Body(...),
    authorization: Annotated[str | None, Header()] = None,
) -> Response:
    """Actualiza los parámetros del artista con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre del artista
        foto (str) : url de la foto miniatura del artista
        historial_canciones (list) : 5 últimas canciones reproducidas por el artista
        playlists (list) : playlists creadas por el artista
        playlists_guardadas (list) : playlists de otros artistas guardadas por el
                                     artista con nombre "nombre"
        canciones_creadas (list) : canciones creadas por el artista

    Returns
    -------
        Response 204 No content

    Raises
    ------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        401
        Not Found 404: No existe un artista con el nombre "nombre"

    """
    try:
        jwt_token = security_service.get_jwt_token_data(authorization)

        artist_service.update_artist(
            name=nombre,
            photo=foto,
            playback_history=historial_canciones,
            playlists=playlists,
            saved_playlists=playlists_guardadas,
            uploaded_songs=canciones_creadas,
            token=jwt_token,
        )
        return Response(None, 204)
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.delete("/{nombre}", tags=["artistas"])
def delete_artista(nombre: str) -> Response:
    """Elimina un artista con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre del artista

    Returns
    -------
        Response 202 Accepted

    Raises
    ------
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Not Found 404: No existe un artista con el nombre "nombre"

    """
    artist_service.delete_artist(nombre)
    return Response(None, 202)


@router.get("/", tags=["artistas"])
def get_artistas() -> Response:
    """Devuelve todos los artistas

    Parameters
    ----------

    Returns
    -------
        Response HTTP_200_OK OK

    Raises
    ------
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe un artista con el nombre "nombre"

    """
    artists = artist_service.get_all_artists()
    artists_dict = {}
    artists_dict["artists"] = jsonable_encoder(artists)

    artists_json = json.dumps(artists_dict)

    return Response(
        artists_json, media_type="application/json", status_code=HTTP_200_OK
    )


@router.get("/{nombre}/reproducciones", tags=["artistas"])
def get_reproducciones_artista(nombre: str) -> Response:
    """Devuelve el número de reproducciones totales de las canciones del artista

    Parameters
    ----------

    Returns
    -------
        Response HTTP_200_OK OK

    Raises
    ------
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe un artista con el nombre "nombre"

    """
    play_count = artist_service.get_play_count_artist(user_name=nombre)

    play_count_json = json_converter_service.get_json_with_iterable_field_from_model(
        play_count, "play_count"
    )

    return Response(
        play_count_json, media_type="application/json", status_code=HTTP_200_OK
    )
