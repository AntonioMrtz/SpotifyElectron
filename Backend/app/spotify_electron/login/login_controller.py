"""
Login controller for handling incoming HTTP Requests
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

import app.auth.auth_service as auth_service
import app.spotify_electron.utils.json_converter.json_converter_utils as json_converter_utils
from app.auth.auth_schema import (
    CreateJWTException,
    JWTValidationException,
    UnexpectedLoginUserException,
    VerifyPasswordException,
)
from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.spotify_electron.login.login_schema import InvalidCredentialsLoginException
from app.spotify_electron.user.base_user_schema import BaseUserNotFoundException

router = APIRouter(
    prefix="/login",
    tags=["Login"],
)


@router.post("/")
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Response:
    """Login user

    Args:
    ----
        form_data (Annotated[OAuth2PasswordRequestForm, Depends): user and password

    """
    try:
        jwt = auth_service.login_user(form_data.username, form_data.password)

        access_token_json = json_converter_utils.get_json_from_model(jwt)
        expiration_date = auth_service.get_token_expire_date()

    except InvalidCredentialsLoginException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
            content=PropertiesMessagesManager.loginInvalidCredentials,
        )
    except (VerifyPasswordException, CreateJWTException):
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.loginVerifyPassword,
        )
    except BaseUserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except (UnexpectedLoginUserException, Exception):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )
    else:
        response = Response(
            access_token_json, media_type="application/json", status_code=HTTP_200_OK
        )
        response.set_cookie(
            key="jwt",
            value=f"Bearer {jwt}",
            httponly=True,
            path="/",
            samesite="none",
            expires=expiration_date,
            secure=True,
        )
        return response


@router.post("/token/{token}")
def login_user_with_jwt(token: str) -> Response:
    """Login user with token

    Args:
        token (str): the user token
    """
    try:
        auth_service.login_user_with_token(token)
    except JWTValidationException:
        return Response(
            status_code=HTTP_403_FORBIDDEN,
            content=PropertiesMessagesManager.tokenInvalidCredentialsAutoLogin,
        )
    except BaseUserNotFoundException:
        return Response(
            status_code=HTTP_404_NOT_FOUND,
            content=PropertiesMessagesManager.userNotFound,
        )
    except (UnexpectedLoginUserException, Exception):
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=PropertiesMessagesManager.commonInternalServerError,
        )
    else:
        response = Response(status_code=HTTP_200_OK)
        return response
