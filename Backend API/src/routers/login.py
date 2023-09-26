from fastapi.responses import Response
from fastapi import APIRouter
import services.login_service as login_service
import json

router = APIRouter(
    prefix="/login",
    tags=["login"],
)


@router.post("/{nombre}", tags=["login"])
def login_usuario(nombre: str,password:str) -> Response:
    """ Devuelve la playlist con nombre "nombre"

    Parameters
    ----------
        nombre (str): Nombre del usuario
        password (str) : Contraseña del usuario

    Returns
    -------
        Response 200 OK + Jwt

    Raises
    -------
        Bad Request 400: "nombre" o "password" es vacío o nulo
        Unauthorized 401 : El usuario o constraseña es incorrecto
        Not Found 404: No existe el usuario
    """

    jwt = login_service.login_user(nombre,password)

    return Response(jwt, media_type="application/json", status_code=200)
