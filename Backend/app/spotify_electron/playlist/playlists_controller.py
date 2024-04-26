from typing import Annotated

from fastapi import APIRouter, Body, Header
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

import app.services.http_encode_service as http_encode_service
import app.spotify_electron.playlist.playlists_service as playlists_service
import app.spotify_electron.security.security_service as security_service
from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.exceptions.http_encode_exceptions import JsonEncodeException
from app.logging.http_encode_logging_constants import ENCODING_ERROR
from app.logging.logging_constants import LOGGING_PLAYLIST_CONTROLLER
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.playlist.playlists_schema import (
    PlaylistBadNameException,
    PlaylistNotFoundException,
    PlaylistServiceException,
)
from app.spotify_electron.security.security_schema import BadJWTTokenProvidedException

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
    ----
        nombre (str): name

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
        playlist_router_logger.exception(f"{ENCODING_ERROR} : {playlist_json}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except (Exception, PlaylistServiceException):
        playlist_router_logger.critical(
            f"{PropertiesMessagesManager.commonInternalServerError}"
        )
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
    """Creates playlist

    Args:
    ----
        name (str): playlist name
        photo (str): photo
        description (str): description
        song_names (list[str], optional): the list of song names. Defaults to Body(...).

    """
    try:
        jwt_token = security_service.get_jwt_token_data(authorization)

        playlists_service.create_playlist(
            name=name,
            photo=photo,
            description=description,
            song_names=song_names,
            token=jwt_token,
        )
        return Response(None, HTTP_201_CREATED)
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except PlaylistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except (Exception, PlaylistServiceException):
        playlist_router_logger.critical(
            f"{PropertiesMessagesManager.commonInternalServerError}"
        )
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
    """Updates playlist data

    Args:
    ----
        name (str): playlist name
        photo (str): photo
        description (str): description
        song_names (list[str], optional): list of song names. Defaults to Body(...).
        new_name (str | None, optional): new name of the playlist. Defaults to None.

    """
    try:
        jwt_token = security_service.get_jwt_token_data(authorization)

        playlists_service.update_playlist(
            name, new_name, photo, description, song_names, jwt_token
        )
        return Response(None, HTTP_204_NO_CONTENT)
    except BadJWTTokenProvidedException:
        return Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except PlaylistBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
        )
    except PlaylistNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
        )
    except (Exception, PlaylistServiceException):
        playlist_router_logger.critical(
            f"{PropertiesMessagesManager.commonInternalServerError}"
        )
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.delete("/{name}", tags=["playlists"])
def delete_playlist(name: str) -> Response:
    """Delete playlist

    Args:
    ----
        name (str): playlist name

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
        playlist_router_logger.critical(
            f"{PropertiesMessagesManager.commonInternalServerError}"
        )
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/", tags=["playlists"])
def get_playlists() -> Response:
    """Return all playlists"""
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
        playlist_router_logger.exception(f"{ENCODING_ERROR} : {playlist_json}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except (Exception, PlaylistServiceException):
        playlist_router_logger.critical(
            f"{PropertiesMessagesManager.commonInternalServerError}"
        )
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/multiple/{names}", tags=["playlists"])
def get_selected_playlists(names: str) -> Response:
    """Return playlists by names

    Args:
    ----
        names (str): names of playlists

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
        playlist_router_logger.exception(f"{ENCODING_ERROR} : {playlist_json}")
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except (Exception, PlaylistServiceException):
        playlist_router_logger.critical(
            f"{PropertiesMessagesManager.commonInternalServerError}"
        )
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
