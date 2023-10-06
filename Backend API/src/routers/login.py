from fastapi.responses import Response
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Union
from datetime import datetime,timedelta,timezone
import json
import services.security_service as security_service


router = APIRouter(
    prefix="/login",
    tags=["login"],
)


DAYS_TO_EXPIRE_COOKIE = 7


@router.post("/", tags=["login"])
def login_usuario(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Response:
    """ Devuelve la playlist con nombre "nombre"

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

    jwt = security_service.login_user(form_data.username, form_data.password)

    access_token_json = json.dumps(jwt)

    utc_timezone = timezone.utc

    # Get the current UTC datetime
    current_utc_datetime = datetime.utcnow().replace(tzinfo=utc_timezone)

    # Calculate expiration date (current UTC datetime + 10 days)
    expiration_date = current_utc_datetime + timedelta(days=DAYS_TO_EXPIRE_COOKIE)

    response = Response(access_token_json, media_type="application/json", status_code=200)
    response.set_cookie(key="jwt", value=jwt, httponly=True, path='/', samesite='None',expires=expiration_date,secure=True)
    #response.set_cookie(key="hola",value="gola",samesite='None',path='/',secure=True)
    #response.set_cookie(key="jwt2", value=jwt, httponly=True, path='/',secure=True,samesite='None')

    return response
