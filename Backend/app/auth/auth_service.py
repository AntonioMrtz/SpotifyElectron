"""
Authentication service for handling business logic
"""

from datetime import UTC, datetime, timedelta, timezone
from typing import Any

import bcrypt
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

import app.spotify_electron.user.base_user_service as base_user_service
from app.auth.auth_schema import (
    BadJWTTokenProvidedException,
    CreateJWTException,
    JWTExpiredException,
    JWTGetUserException,
    JWTMissingCredentialsException,
    JWTNotProvidedException,
    JWTValidationException,
    TokenData,
    UnexpectedLoginUserException,
    UserUnauthorizedException,
    VerifyPasswordException,
)
from app.common.app_schema import AppEnviroment
from app.common.PropertiesManager import PropertiesManager
from app.exceptions.base_exceptions_schema import BadParameterException
from app.logging.logging_constants import LOGGING_AUTH_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.login.login_schema import InvalidCredentialsLoginException
from app.spotify_electron.user.base_user_service import validate_user_should_exists
from app.spotify_electron.user.user.user_schema import (
    UserDTO,
    UserNotFoundException,
    UserServiceException,
)
from app.spotify_electron.utils.validations.validation_utils import validate_parameter

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 days
DAYS_TO_EXPIRE_COOKIE = 7


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/whoami/")

auth_service_logger = SpotifyElectronLogger(LOGGING_AUTH_SERVICE).getLogger()


def create_access_token(data: dict[str, str], expires_delta: timedelta | None = None) -> str:
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
            getattr(PropertiesManager, AppEnviroment.SECRET_KEY_SIGN_ENV_NAME),
            algorithm=ALGORITHM,
        )
    except Exception as exception:
        raise CreateJWTException from exception
    else:
        auth_service_logger.info(f"JWT created from data : {data}")
        return encoded_jwt


def get_jwt_token_data(
    token_raw_data: str,
) -> TokenData:
    """Decrypt jwt data and returns data from it

    Args:
    ----
        token_raw_data (TokenData): JWT Token

    Raises:
    ------
        BadJWTTokenProvidedException: invalid token provided

    Returns:
    -------
        TokenData: the data provided by the JWT Token

    """
    validate_token_exists(token_raw_data)
    try:
        payload = jwt.decode(
            token_raw_data,  # type: ignore
            getattr(PropertiesManager, AppEnviroment.SECRET_KEY_SIGN_ENV_NAME),
            algorithms=[ALGORITHM],
        )
        username = payload.get("access_token")
        role = payload.get("role")
        token_type = payload.get("token_type")

        credentials = [username, role, token_type]
        validate_jwt_credentials_missing(credentials)
        token_data = TokenData(username=username, role=role, token_type=token_type)  # type: ignore

    except JWTNotProvidedException as exception:
        auth_service_logger.exception("No JWT Token was provided")
        raise BadJWTTokenProvidedException from exception
    except JWTMissingCredentialsException as exception:
        auth_service_logger.exception(
            f"One or more credentials obtained from JWT are missing : {credentials}"
        )
        raise BadJWTTokenProvidedException from exception
    except JWTError as exception:
        auth_service_logger.exception("Error decoding JWT Token")
        raise BadJWTTokenProvidedException from exception
    except Exception as exception:
        auth_service_logger.exception("Unexpected error getting data from JWT Token")
        raise BadJWTTokenProvidedException from exception
    else:
        auth_service_logger.info(f"Token data : {token_data}")
        return token_data


def get_current_user(
    token: TokenData,
) -> UserDTO:
    """Get current user from JWT Token

    Args:
    ----
        token (TokenData): the token

    Raises:
    ------
        UserNotFoundException: token user not found
        JWTGetUserException: if error while retrieving user from token
    Returns:
        Artist | User: the user or artist associated with the JWT Token

    """
    try:
        jwt_username = token.username

        user = base_user_service.get_user(jwt_username)
    except BadJWTTokenProvidedException as exception:
        auth_service_logger.exception("Error getting jwt token data")
        raise BadJWTTokenProvidedException from exception
    except UserNotFoundException as exception:
        auth_service_logger.exception(f"User {jwt_username} not found")
        raise UserNotFoundException from exception
    except Exception as exception:
        auth_service_logger.exception(f"Unexpected exception getting user from token {token}")
        raise JWTGetUserException from exception
    else:
        auth_service_logger.info(f"Get Current User successful : {jwt_username}")
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
        validate_parameter(name)
        validate_parameter(password)
        validate_user_should_exists(name)

        user_type = base_user_service.get_user_type(user_name=name)
        user_password = base_user_service.get_user_password(user_name=name)

        verify_password(password, user_password)

        jwt_data = {
            "access_token": name,
            "role": user_type.value,
            "token_type": "bearer",
        }
        access_token_data = create_access_token(jwt_data)

    except BadParameterException as exception:
        auth_service_logger.exception("Invalid login credentials")
        raise InvalidCredentialsLoginException from exception
    except VerifyPasswordException as exception:
        auth_service_logger.exception("Passwords Validation failed : passwords dont match")
        raise VerifyPasswordException from exception
    except CreateJWTException as exception:
        auth_service_logger.exception(f"Error creating JWT Token from data : {jwt_data}")
        raise VerifyPasswordException from exception
    except UserNotFoundException as exception:
        auth_service_logger.exception(f"User {name} doesnt exists")
        raise UserNotFoundException from exception
    except UserServiceException as exception:
        auth_service_logger.exception(
            f"Unexpected error in User service while login user : {name}"
        )
        raise UnexpectedLoginUserException from exception
    except Exception as exception:
        auth_service_logger.exception(f"Unexpected error login user : {name}")
        raise UnexpectedLoginUserException from exception
    else:
        auth_service_logger.info(f"User {name} logged successfully")
        return access_token_data


def validate_jwt(token: str) -> None:
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
            token,
            getattr(PropertiesManager, AppEnviroment.SECRET_KEY_SIGN_ENV_NAME),
            ALGORITHM,
        )
        validate_token_is_expired(decoded_token)

    except JWTError as exception:
        auth_service_logger.exception(f"Error decoding token : {token}")
        raise JWTValidationException from exception

    except JWTExpiredException as exception:
        auth_service_logger.exception(f"Token is expired : {token}")
        raise JWTValidationException from exception

    except Exception as exception:
        auth_service_logger.exception(f"Unexpected error validating token : {token}")
        raise JWTValidationException from exception


def validate_jwt_user_matches_user(token: TokenData, user_name: str):
    """Validates if user matches the jwt user

    Args:
        token (TokenData): jwt token
        user_name (str): user

    Raises:
        UserUnauthorizedException: if the user didnt match the jwt user
    """
    if not token.username == user_name:
        raise UserUnauthorizedException


def validate_token_is_expired(token: dict[str, Any]) -> None:
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


def validate_token_exists(token: Any) -> None:
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


def validate_jwt_credentials_missing(credentials: list[Any]):
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
