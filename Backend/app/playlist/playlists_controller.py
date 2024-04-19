from typing import Annotated

from fastapi import APIRouter, Body, Header, HTTPException
from fastapi.responses import Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

import app.playlist.playlists_service as playlists_service
import app.services.http_encode_service as http_encode_service
import app.services.security_service as security_service
from app.exceptions.http_encode_exceptions import JsonEncodeException
from app.logging.commons_logging_constants import INTERNAL_SERVER_ERROR
from app.logging.http_encode_logging_constants import ENCODING_ERROR
from app.logging.logger_constants import LOGGING_PLAYLIST_CONTROLLER
from app.logging.logging_schema import SpotifyElectronLogger
from app.playlist.playlists_schema import (
    PlaylistBadNameException,
    PlaylistNotFoundException,
    PlaylistServiceException,
)

router = APIRouter(
    prefix="/playlists",
    tags=["Playlists"],
)

playlist_router_logger = SpotifyElectronLogger(LOGGING_PLAYLIST_CONTROLLER).getLogger()

# TODO set in content of Responses messages of error from messages.ini


@router.get("/{name}", tags=["playlists"])
def get_playlist(name: str) -> Response:
    """Gets playlist by name

    Args:
        nombre (str): name

    Returns:
        Response: _description_
    """

    try:
        playlist = playlists_service.get_playlist(name)
        playlist_json = http_encode_service.get_json(playlist)

        return Response(
            playlist_json, media_type="application/json", status_code=HTTP_200_OK
        )

    except PlaylistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except JsonEncodeException:
        playlist_router_logger.exception(f"{ENCODING_ERROR}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except (Exception, PlaylistServiceException):
        playlist_router_logger.critical(f"{INTERNAL_SERVER_ERROR}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/", tags=["playlists"])
def post_playlist(
    name: str,
    photo: str,
    description: str,
    song_names: list[str] = Body(...),
    authorization: Annotated[str | None, Header()] = None,
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
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Authorization header is missing"
        )

    try:
        jwt_token = security_service.get_jwt_token(authorization)

        playlists_service.create_playlist(
            name=name,
            photo=photo,
            description=description,
            song_names=song_names,
            token=jwt_token,
        )

        return Response(None, HTTP_201_CREATED)
    except PlaylistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except (Exception, PlaylistServiceException):
        playlist_router_logger.critical(f"{INTERNAL_SERVER_ERROR}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.put("/{name}", tags=["playlists"])
def update_playlist(
    name: str,
    photo: str,
    description: str,
    song_names: list[str] = Body(...),
    new_name: str | None = None,
    authorization: Annotated[str | None, Header()] = None,
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

        playlists_service.update_playlist(
            name, new_name, photo, description, song_names, jwt_token
        )
        return Response(None, HTTP_204_NO_CONTENT)
    except PlaylistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except (Exception, PlaylistServiceException):
        playlist_router_logger.critical(f"{INTERNAL_SERVER_ERROR}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.delete("/{name}", tags=["playlists"])
def delete_playlist(name: str) -> Response:
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
        playlists_service.delete_playlist(name)
        return Response(status_code=HTTP_202_ACCEPTED)
    except PlaylistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except (Exception, PlaylistServiceException):
        playlist_router_logger.critical(f"{INTERNAL_SERVER_ERROR}")
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
        playlists = playlists_service.get_all_playlist()
        playlist_json = http_encode_service.get_json_with_iterable_field(
            playlists, "playlists"
        )

        return Response(
            playlist_json, media_type="application/json", status_code=HTTP_200_OK
        )
    except PlaylistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except JsonEncodeException:
        playlist_router_logger.exception(f"{ENCODING_ERROR}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except (Exception, PlaylistServiceException):
        playlist_router_logger.critical(f"{INTERNAL_SERVER_ERROR}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/multiple/{names}", tags=["playlists"])
def get_selected_playlists(names: str) -> Response:
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
        playlists = playlists_service.get_selected_playlists(names.split(","))

        playlist_json = http_encode_service.get_json_with_iterable_field(
            playlists, "playlists"
        )

        return Response(
            playlist_json, media_type="application/json", status_code=HTTP_200_OK
        )
    except PlaylistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except JsonEncodeException:
        playlist_router_logger.exception(f"{ENCODING_ERROR}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except (Exception, PlaylistServiceException):
        playlist_router_logger.critical(f"{INTERNAL_SERVER_ERROR}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
