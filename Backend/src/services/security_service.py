from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, Union
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from services.user_service import get_user
from model.TokenData import TokenData
from model.Artist import Artist
from model.User import User
from services.utils import checkValidParameterString
from services.all_users_service import check_user_exists, isArtistOrUser
from services.artist_service import get_artist
from services.user_service import get_user
from model.UserType import User_Type
import services.user_service as user_service
import services.artist_service as artist_service
import os
import json
import bcrypt

SECRET_KEY = os.getenv("SECRET_KEY_SIGN")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080 # 7 days

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/whoami/")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """ Create a jwt token from data with a expire date

    Parameters
    ----------
        data (dict): Info to be stored in the token
        expires_delta (timedelta) : Expire time of the token

    Raises
    -------
        JWTError

    Returns
    -------
        Jwt token
    """

    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except JWTError:
        raise HTTPException(status_code=401, detail="Credenciales inválidos")


def get_jwt_token(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    """ Decrypt jwt data and returns data from it

    Parameters
    ----------
        token (jwt token)

    Raises
    -------
        401 : Bad credentials

    Returns
    -------
        TokenData
    """

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
        token_data = TokenData(
            username=username, role=role, token_type=token_type)
        return token_data

    except JWTError:
        raise HTTPException(status_code=401, detail="Credenciales inválidos")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> Union[Artist, User]:
    """ From a jwt token returns the User or the Artist

    Parameters
    ----------
        token (jwt token)

    Raises
    -------
        400 : Bad Request
        401 : Bad credentials
        404 : User not found

    Returns
    -------
        Jwt token
    """

    jwt: TokenData = get_jwt_token(token)

    if jwt.token_type == User_Type.ARTIST:
        user = get_artist(jwt.username)

    else:
        user = get_user(jwt.username)

    if user is None:
        raise credentials_exception
    return user


def login_user(name: str, password: str) -> json:
    """ Checks user credentials and return a jwt token"

    Parameters
    ----------
        name (str): Users's name
        password (str) : password of the user

    Raises
    -------
        400 : Bad Request
        401 : Bad credentials
        404 : User not found
        JWTError

    Returns
    -------
        Jwt token
    """

    if not checkValidParameterString(name) or not checkValidParameterString(password):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    if not check_user_exists(user_name=name):
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if isArtistOrUser(user_name=name) == User_Type.ARTIST:
        user = get_artist(name)
        user_type = User_Type.ARTIST

    else:
        user = get_user(name)
        user_type = User_Type.USER

    # check password

    utf8_password = user.password

    if not bcrypt.checkpw(password.encode('utf-8'), utf8_password):
        raise HTTPException(
            status_code=401, detail="Las credenciales no son válidas")

    jwt_data = {

        'access_token': name,
        'role': user_type.value,
        "token_type": "bearer",

    }

    jwt = create_access_token(jwt_data)

    return jwt


def check_jwt_is_valid(token: str):

    try:
        # Decode the JWT
        decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)

        # Verify the expiration time
        expiration_time = datetime.utcfromtimestamp(decoded_token["exp"])
        if expiration_time < datetime.utcnow():
            return False  # Token has expired

        # Additional checks can be added here (e.g., issuer, audience)

        return True  # Token is valid

    except:
        return False  # Token has expired or is invalid
