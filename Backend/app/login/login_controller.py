from datetime import UTC, datetime, timedelta
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

import app.security.security_service as security_service
import app.services.http_encode_service as http_encode_service
from app.login.login_schema import InvalidCredentialsLoginException
from app.security.security_schema import (
    CreateJWTException,
    UnexpectedLoginUserException,
    VerifyPasswordException,
)
from app.user.user_schema import UserNotFoundException

router = APIRouter(
    prefix="/login",
    tags=["login"],
)


DAYS_TO_EXPIRE_COOKIE = 7


@router.post("/", tags=["login"])
def login_usuario(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Response:
    """Devuelve la playlist con nombre "nombre"

    Parameters
    ----------
        form_data.username (str): Nombre del usuario
        form_data.password (str) : Contraseña del usuario

    Returns
    -------
        Response 200 OK + Jwt

    Raises
    -------
        Bad Request 400: "nombre" o "password" es vacío o nulo
        Unauthorized 401 : El usuario o constraseña es incorrecto
        Not Found 404: No existe el usuario
    """

    try:
        jwt = security_service.login_user(form_data.username, form_data.password)

        access_token_json = http_encode_service.get_json(jwt)

        # Get the current UTC datetime
        current_utc_datetime = datetime.now(UTC).replace(tzinfo=UTC)

        # Calculate expiration date (current UTC datetime + 10 days)
        expiration_date = current_utc_datetime + timedelta(days=DAYS_TO_EXPIRE_COOKIE)

        # response.set_cookie(key="hola",value="gola",samesite='None',path='/',secure=True)
        # response.set_cookie(key="jwt2", value=jwt, httponly=True, path='/',secure=True,samesite='None')
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
