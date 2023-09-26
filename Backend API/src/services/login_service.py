from fastapi import HTTPException
from services.utils import checkValidParameterString
from services.all_users_service import check_user_exists,isArtistOrUser
from services.artist_service import get_artist
from services.user_service import get_user
from model.UserType import User_Type
import json
import bcrypt



def login_user(name: str,password:str) -> json:
    """ Returns a Playlist with his songs"

    Parameters
    ----------
        name (str): Users's name
        password (str) : password of the user

    Raises
    -------
        400 : Bad Request
        401 : Bad credentials
        404 : User not found

    Returns
    -------
        Jwt token
    """

    if not checkValidParameterString(name) or not checkValidParameterString(password):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    if not check_user_exists(user_name=name):
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if isArtistOrUser==User_Type.ARTIST:
        user = get_artist(name)
        user_type = User_Type.ARTIST

    else:
        user = get_user(name)
        user_type = User_Type.USER


    # check password

    utf8_password = user.password

    if not bcrypt.checkpw(password.encode('utf-8'),utf8_password) :
        raise HTTPException(status_code=401, detail="Las credenciales no son válidas")

    jwt = {

        'user': name,
        'role': user_type.value

    }

    jwt_json = json.dumps(jwt)


    return jwt_json




