from fastapi.responses import Response
from fastapi import APIRouter,Security, Depends , Header , HTTPException , status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Union
from jose import JWTError, jwt
from datetime import datetime, timedelta
import services.login_service as login_service
import json
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from services.user_service import get_user


SECRET_KEY = os.getenv("SECRET_KEY_SIGN")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


router = APIRouter(
    prefix="/login",
    tags=["login"],
)

@dataclass
class TokenData():
    username: str
    role: str
    token_type : str


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("access_token")
        role: str = payload.get("role")
        token_type: str = payload.get("token_type")
        if username is None or role is None or token_type is None:
            raise credentials_exception
        token_data = TokenData(username=username,role=role,token_type=token_type)
    except JWTError:
        raise credentials_exception
    user = get_user(name=username)
    if user is None:
        raise credentials_exception
    return user



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


@router.get("/", tags=["login"])
def whomai(authorization: Annotated[Union[str, None], Header()] = None) -> Response:

    if authorization is None:
            raise HTTPException(status_code=401, detail="Authorization header is missing")

    user = get_current_user(authorization)
    usuario_json = user.get_json()

    return Response(usuario_json, media_type="application/json", status_code=200)
