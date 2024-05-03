from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

import app.spotify_electron.security.security_service as security_service
import app.spotify_electron.utils.json_converter.json_converter_service as json_converter_service
from app.spotify_electron.login.login_schema import InvalidCredentialsLoginException
from app.spotify_electron.security.security_schema import (
    CreateJWTException,
    UnexpectedLoginUserException,
    VerifyPasswordException,
)
from app.spotify_electron.user.user_schema import UserNotFoundException

router = APIRouter(
    prefix="/login",
    tags=["Login"],
)


@router.post("/", tags=["login"])
def login_usuario(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Response:
    """Login user

    Args:
    ----
        form_data (Annotated[OAuth2PasswordRequestForm, Depends): user and password

    """
    try:
        jwt = security_service.login_user(form_data.username, form_data.password)

        access_token_json = json_converter_service.get_json_from_model(jwt)
        expiration_date = security_service.get_token_expire_date()

    except InvalidCredentialsLoginException:
        return Response(
            media_type="application/json",
            status_code=HTTP_400_BAD_REQUEST,
        )
    except (VerifyPasswordException, CreateJWTException):
        return Response(
            media_type="application/json",
            status_code=HTTP_401_UNAUTHORIZED,
        )
    except UserNotFoundException:
        return Response(
            media_type="application/json",
            status_code=HTTP_404_NOT_FOUND,
        )
    except (UnexpectedLoginUserException, Exception):
        return Response(
            media_type="application/json",
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
    else:
        response = Response(
            access_token_json, media_type="application/json", status_code=HTTP_200_OK
        )
        response.set_cookie(
            key="jwt",
            value=jwt,
            httponly=True,
            path="/",
            samesite="none",
            expires=expiration_date,
            secure=True,
        )
        return response
