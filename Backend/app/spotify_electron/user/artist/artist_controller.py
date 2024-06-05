import json

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

import app.spotify_electron.user.artist.artist_service as artist_service
import app.spotify_electron.utils.json_converter.json_converter_utils as json_converter_utils
from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.exceptions.base_exceptions_schema import JsonEncodeException
from app.spotify_electron.user.user.user_schema import (
    UserAlreadyExistsException,
    UserBadNameException,
    UserNotFoundException,
    UserServiceException,
)

router = APIRouter(
    prefix="/artists",
    tags=["Artists"],
)


@router.get("/{name}")
def get_artist(name: str) -> Response:
    """Get artist by name

    Args:
        name (str): artist name
    """
    try:
        artist = artist_service.get_artist(name)
        artist_json = json_converter_utils.get_json_from_model(artist)

        return Response(
            artist_json, media_type="application/json", status_code=HTTP_200_OK
        )

    except UserBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.artistBadName,
        )
    except UserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.artistNotFound,
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, UserServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.post("/")
def create_artist(name: str, photo: str, password: str) -> Response:
    """Create artist

    Args:
        name (str): artist name
        photo (str): artist photo
        password (str): artist password
    """
    try:
        artist_service.create_artist(name, photo, password)
        return Response(None, 201)
    except (UserBadNameException, UserAlreadyExistsException):
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.artistBadName,
        )
    except UserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.artistNotFound,
        )
    except (Exception, UserServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/")
def get_artists() -> Response:
    """Get all artists"""
    try:
        artists = artist_service.get_all_artists()
        artists_dict = {}
        artists_dict["artists"] = jsonable_encoder(artists)

        artists_json = json.dumps(artists_dict)

        return Response(
            artists_json, media_type="application/json", status_code=HTTP_200_OK
        )
    except UserBadNameException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.artistBadName,
        )
    except UserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.artistNotFound,
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, UserServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )


@router.get("/{name}/playbacks")
def get_playback_count(name: str) -> Response:
    """Get artist total playback count of his songs"""
    try:
        play_count = artist_service.get_playback_count_artist(user_name=name)

        play_count_json = json_converter_utils.get_json_with_iterable_field_from_model(
            play_count, "play_count"
        )

        return Response(
            play_count_json, media_type="application/json", status_code=HTTP_200_OK
        )
    except JsonEncodeException:
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonEncodingError,
        )
    except (Exception, UserServiceException):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )
