from fastapi.responses import Response
from fastapi import APIRouter,Security, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Union
from jose import JWTError, jwt
from datetime import datetime, timedelta
import services.login_service as login_service
import json
import os
from dotenv import load_dotenv

SECRET_KEY = os.getenv("SECRET_KEY_SIGN")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

load_dotenv()

router = APIRouter(
    prefix="/login",
    tags=["login"],
)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



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


    jwt = login_service.login_user(form_data.username,form_data.password)

    access_token = create_access_token(jwt)

    access_token_json = json.dumps(access_token)

    return Response(access_token_json, media_type="application/json", status_code=200)

