from fastapi.responses import Response
from fastapi import APIRouter, Depends  , HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Union
import json
import services.security_service as security_service


router = APIRouter(
    prefix="/login",
    tags=["login"],
)



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


    jwt = security_service.login_user(form_data.username,form_data.password)

    access_token = security_service.create_access_token(jwt)

    access_token_json = json.dumps(access_token)

    return Response(access_token_json, media_type="application/json", status_code=200)


