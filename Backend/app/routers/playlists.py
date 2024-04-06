from typing import Annotated, List, Optional, Union

import app.services.http_encode_service as http_encode_service
import app.services.playlist_service as playlist_service
import app.services.security_service as security_service
from app.exceptions.http_encode_exceptions import JsonEncodeException
from app.exceptions.repository_exceptions import ItemNotFoundException
from app.exceptions.services_exceptions import BadParameterException
from app.logging.commons_logging_constants import INTERNAL_SERVER_ERROR
from app.logging.http_encode_logging_constants import ENCODING_ERROR
from app.logging.logger_constants import LOGGING_PLAYLISTS_ROUTER
from app.logging.logging_schema import SpotifyElectronLogger
from fastapi import APIRouter, Body, Header, HTTPException
from fastapi.responses import Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

router = APIRouter(
    prefix="/playlists",
    tags=["playlists"],
)

playlist_router_logger = SpotifyElectronLogger(LOGGING_PLAYLISTS_ROUTER).getLogger()


@router.get("/{nombre}", tags=["playlists"])
def get_playlist(nombre: str) -> Response:
    """Devuelve la playlist con nombre "nombre"

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

    try:
        playlist = playlist_service.get_playlist(nombre)
        playlist_json = http_encode_service.get_json(playlist)

        return Response(
            playlist_json, media_type="application/json", status_code=HTTP_200_OK
        )

    except BadParameterException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
        )
    except ItemNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except JsonEncodeException as error:
        playlist_router_logger.error(f"{ENCODING_ERROR} :{error}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except Exception as error:
        playlist_router_logger.error(f"{INTERNAL_SERVER_ERROR} :{error}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/", tags=["playlists"])
def post_playlist(
    nombre: str,
    foto: str,
    descripcion: str,
    nombres_canciones: List[str] = Body(...),
    authorization: Annotated[Union[str, None], Header()] = None,
) -> Response:
    """Registra la playlist

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
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    try:
        jwt_token = security_service.get_jwt_token(authorization)

        playlist_service.create_playlist(
            name=nombre,
            photo=foto,
            description=descripcion,
            song_names=nombres_canciones,
            token=jwt_token,
        )

        return Response(None, 201)
    except BadParameterException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
        )
    except ItemNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except Exception as error:
        playlist_router_logger.error(f"{INTERNAL_SERVER_ERROR} :{error}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.put("/{nombre}", tags=["playlists"])
def update_playlist(
    nombre: str,
    foto: str,
    descripcion: str,
    nombres_canciones: List[str] = Body(...),
    nuevo_nombre: Optional[str] = None,
    authorization: Annotated[Union[str, None], Header()] = None,
) -> Response:
    """Actualiza los parámetros de la playlist con nombre "nombre" ,
    las canciones repetidas son serán añadidas

    Parameters
    ----------
        nombre (str): Nombre de la playlist
        nombres_canciones (list) : Lista con las canciones de la playlist
        foto (str) : url de la foto miniatura de la playlist
        nuevo_nombre (str Opcional [default = None]) : Nuevo nombre de la playlist,
                                                       si es vacío no se actualiza
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
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    try:
        jwt_token = security_service.get_jwt_token(authorization)

        playlist_service.update_playlist(
            nombre, nuevo_nombre, foto, descripcion, nombres_canciones, jwt_token
        )
        return Response(None, 204)
    except BadParameterException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
        )
    except ItemNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except Exception as error:
        playlist_router_logger.error(f"{INTERNAL_SERVER_ERROR} :{error}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.delete("/{nombre}", tags=["playlists"])
def delete_playlist(nombre: str) -> Response:
    """Elimina una playlist con nombre "nombre"

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

    try:
        playlist_service.delete_playlist(nombre)
        return Response(None, 202)
    except BadParameterException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
        )
    except ItemNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except Exception as error:
        playlist_router_logger.error(f"{INTERNAL_SERVER_ERROR} :{error}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/", tags=["playlists"])
def get_playlists() -> Response:
    """Devuelve todas las playlists [ SOLO nombres canciones , no el archivo de audio ]

    Parameters
    ----------

    Returns
    -------
        Response 200 OK

    Raises
    -------
    """
    try:
        playlists = playlist_service.get_all_playlist()
        playlist_json = http_encode_service.get_json_with_iterable_field(
            playlists, "playlists"
        )

        return Response(playlist_json, media_type="application/json", status_code=200)
    except BadParameterException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
        )
    except ItemNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except JsonEncodeException as error:
        playlist_router_logger.error(f"{ENCODING_ERROR} :{error}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except Exception as error:
        playlist_router_logger.error(f"{INTERNAL_SERVER_ERROR} :{error}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/multiple/{nombres}", tags=["playlists"])
def get_selected_playlists(nombres: str) -> Response:
    """Devuelve todas las playlists [ SOLO nombres canciones , no el archivo de audio ]

    Parameters
    ----------

    Returns
    -------
        Response 200 OK

    Raises
    -------
    """

    try:
        playlists = playlist_service.get_selected_playlists(nombres.split(","))

        playlist_json = http_encode_service.get_json_with_iterable_field(
            playlists, "playlists"
        )

        return Response(playlist_json, media_type="application/json", status_code=200)
    except BadParameterException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
        )
    except ItemNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except JsonEncodeException as error:
        playlist_router_logger.error(f"{ENCODING_ERROR} :{error}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except Exception as error:
        playlist_router_logger.error(f"{INTERNAL_SERVER_ERROR} :{error}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
