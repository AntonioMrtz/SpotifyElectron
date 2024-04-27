from datetime import UTC, datetime, timedelta, timezone
from typing import Annotated, Any

import bcrypt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

import app.services.all_users_service as all_users_service
import app.services.artist_service as artist_service
import app.services.user_service as user_service
from app.common.PropertiesManager import PropertiesManager
from app.constants.set_up_constants import DISTRIBUTION_ID_ENV_NAME
from app.exceptions.exceptions_schema import BadParameterException
from app.logging.logging_constants import LOGGING_SECURITY_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.model.Artist import Artist
from app.model.User import User
from app.model.UserType import User_Type
from app.services.utils import checkValidParameterString
from app.spotify_electron.login.login_schema import InvalidCredentialsLoginException
from app.spotify_electron.playlist.playlists_service import handle_user_should_exists
from app.spotify_electron.security.security_schema import (
    BadJWTTokenProvidedException,
    CreateJWTException,
    JWTExpiredException,
    JWTGetUserException,
    JWTMissingCredentialsException,
    JWTNotProvidedException,
    JWTValidationException,
    TokenData,
    UnexpectedLoginUserException,
    VerifyPasswordException,
)
from app.spotify_electron.user.user_schema import UserNotFoundException

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 days
DAYS_TO_EXPIRE_COOKIE = 7


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/whoami/")

security_service_logger = SpotifyElectronLogger(LOGGING_SECURITY_SERVICE).getLogger()


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a jwt token from data with a expire date

    Args:
    ----
        data (dict): Info to be stored in the token
        expires_delta (timedelta | None, optional): Expire date of the token

    Raises:
    ------
        CreateJWTException: if an error ocurred creating JWT Token

    Returns:
    -------
        str: the JWT Token created

    """
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta  # noqa: UP017 TODO
        else:
            expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # noqa: UP017 TODO
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            getattr(PropertiesManager, DISTRIBUTION_ID_ENV_NAME),
            algorithm=ALGORITHM,
        )
    except Exception as exception:
        raise CreateJWTException from exception
    else:
        security_service_logger.info(f"JWT created from data : {data}")
        return encoded_jwt


def get_jwt_token_data(
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> TokenData:
    """Decrypt jwt data and returns data from it

    Args:
    ----
        token (Annotated[str  |  None, Depends): JWT Token

    Raises:
    ------
        BadJWTTokenProvidedException: invalid token provided

    Returns:
    -------
        TokenData: the data provided by the JWT Token

    """
    hanle_incoming_jwt_token(token)
    try:
        payload = jwt.decode(
            token,  # type: ignore
            getattr(PropertiesManager, DISTRIBUTION_ID_ENV_NAME),
            algorithms=[ALGORITHM],
        )
        username = payload.get("access_token")
        role = payload.get("role")
        token_type = payload.get("token_type")

        credentials = [username, role, token_type]
        check_are_jwt_credentials_missing(credentials)
        token_data = TokenData(username=username, role=role, token_type=token_type)  # type: ignore

    except JWTNotProvidedException as exception:
        security_service_logger.exception("No JWT Token was provided")
        raise BadJWTTokenProvidedException from exception
    except JWTMissingCredentialsException as exception:
        security_service_logger.exception(
            f"One or more credentials obtained from JWT are missing : {credentials}"
        )
        raise BadJWTTokenProvidedException from exception
    except JWTError as exception:
        security_service_logger.exception("Error decoding JWT Token")
        raise BadJWTTokenProvidedException from exception
    except Exception as exception:
        security_service_logger.exception(
            "Unexpected error getting data from JWT Token"
        )
        raise BadJWTTokenProvidedException from exception
    else:
        security_service_logger.info(f"Token data : {token_data}")
        return token_data


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> Artist | User:
    """Get current user from JWT Token

    Args:
    ----
        token (Annotated[str, Depends): the token

    Raises:
    ------
        UserNotFoundException: token user not found
        JWTGetUserException: if error while retrieving user from token
    Returns:
        Artist | User: the user or artist associated with the JWT Token

    """
    try:
        jwt = get_jwt_token_data(token)

        if jwt.role == User_Type.ARTIST:
            user = artist_service.get_artist(jwt.username)
        elif jwt.role == User_Type.USER:
            user = user_service.get_user(jwt.username)
    except BadJWTTokenProvidedException as exception:
        security_service_logger.exception("Error getting jwt token data")
        raise BadJWTTokenProvidedException from exception
    except UserNotFoundException as exception:
        security_service_logger.exception(f"User {jwt.username} not found")
        raise UserNotFoundException from exception
    except Exception as exception:
        security_service_logger.exception(
            f"Unexpected exception getting user from token {token}"
        )
        raise JWTGetUserException from exception
    else:
        security_service_logger.info(f"Get Current User successful : {user}")
        return user


def hash_password(plain_password: str) -> bytes:
    """Hash a password with a randomly-generated salt

    Args:
    ----
        plain_password (str): plain text password

    Returns:
    -------
        bytes: the hashed password

    """
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())


def verify_password(plain_password: str, hashed_password: bytes):
    """Verifies if plan text password is the same as a hashed password

    Args:
    ----
        plain_password (str): plain text password
        hashed_password (bytes): hashed password

    Raises:
    ------
        VerifyPasswordException: if passwords dont match

    """
    if not bcrypt.checkpw(plain_password.encode(), hashed_password):
        raise VerifyPasswordException


def get_token_expire_date() -> datetime:
    """Returns expire date for new token

    Returns
    -------
        datetime: the expire date for the token

    """
    current_utc_datetime = datetime.now(timezone.utc).replace(tzinfo=timezone.utc)  # noqa: UP017 TODO
    return current_utc_datetime + timedelta(days=DAYS_TO_EXPIRE_COOKIE)


def login_user(name: str, password: str) -> str:
    """Checks user credentials and return a jwt token

    Args:
    ----
        name (str): Users's name
        password (str): Users's password

    Raises:
    ------
        InvalidCredentialsLoginException: bad user credentials
        VerifyPasswordException: failing authenticating user and password
        UserNotFoundException: user doesnt exists
        UnexpectedLoginUserException: unexpected error during user login

    Returns:
    -------
        str: the JWT Token

    """
    try:
        checkValidParameterString(name)
        checkValidParameterString(password)

        # TODO
        handle_user_should_exists(name)

        # TODO unificar y tratar excepciones
        if all_users_service.isArtistOrUser(user_name=name) == User_Type.ARTIST:
            user = artist_service.get_artist(name)
            user_type = User_Type.ARTIST

        else:
            user = user_service.get_user(name)
            user_type = User_Type.USER

        verify_password(password, user.password)

        jwt_data = {
            "access_token": name,
            "role": user_type.value,
            "token_type": "bearer",
        }
        access_token_data = create_access_token(jwt_data)

    except BadParameterException as exception:
        security_service_logger.exception("Invalid login credentials")
        raise InvalidCredentialsLoginException from exception
    except VerifyPasswordException as exception:
        security_service_logger.exception(
            "Passwords Validation failed : passwords dont match"
        )
        raise VerifyPasswordException from exception
    except CreateJWTException as exception:
        security_service_logger.exception(
            f"Error creating JWT Token from data : {jwt_data}"
        )
        raise VerifyPasswordException from exception
    except UserNotFoundException as exception:
        security_service_logger.exception(f"User {name} doesnt exists")
        raise UserNotFoundException from exception
    except Exception as exception:
        security_service_logger.exception(f"Unexpected error login user : {name}")
        raise UnexpectedLoginUserException from exception
    else:
        security_service_logger.info(f"User {name} logged successfully")
        return access_token_data


def check_jwt_is_valid(token: str) -> None:
    """Check if JWT token is valid

    Args:
    ----
        token (str): the token to validate

    Raises:
    ------
        JWTValidationException: if the validation was not succesfull

    """
    try:
        decoded_token = jwt.decode(
            token, getattr(PropertiesManager, DISTRIBUTION_ID_ENV_NAME), ALGORITHM
        )
        check_token_is_expired(decoded_token)

    except JWTError as exception:
        security_service_logger.exception(f"Error decoding token : {token}")
        raise JWTValidationException from exception

    except JWTExpiredException as exception:
        security_service_logger.exception(f"Token is expired : {token}")
        raise JWTValidationException from exception

    except Exception as exception:
        security_service_logger.exception(
            f"Unexpected error validating token : {token}"
        )
        raise JWTValidationException from exception


def check_token_is_expired(token: dict) -> None:
    """Checks if token is expired comparing current date with expiration date

    Args:
    ----
        token (dict): token to check

    Raises:
    ------
        JWTExpiredException: if token is expired

    """
    expiration_time = datetime.fromtimestamp(token["exp"], timezone.utc)  # noqa: UP017 TODO
    if expiration_time < datetime.now(timezone.utc):  # noqa: UP017 TODO
        raise JWTExpiredException


def hanle_incoming_jwt_token(token: Any) -> None:
    """Check whether jwt token is None or not

    Args:
    ----
        token (Any): the incoming token

    Raises:
    ------
        JWTNotProvidedException: if the token is None

    """
    if token is None:
        raise JWTNotProvidedException


def check_are_jwt_credentials_missing(credentials: list[Any]):
    """Check if any jwt credentials are missing

    Args:
    ----
        credentials (list[str]): list with the obtained credentials

    Raises:
    ------
        JWTMissingCredentialsException: if a credential is missing

    """
    for credential in credentials:
        if credential is None:
            raise JWTMissingCredentialsException
