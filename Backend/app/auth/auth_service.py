"""
Authentication service for handling business logic
"""

from datetime import UTC, datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt

import app.spotify_electron.user.base_user_service as base_user_service
import app.spotify_electron.user.validations.base_user_service_validations as base_user_service_validations  # noqa: E501
from app.auth.auth_schema import (
    AuthConfig,
    BadJWTTokenProvidedError,
    CreateJWTError,
    JWTExpiredError,
    JWTMissingCredentialsError,
    JWTNotProvidedError,
    JWTValidationError,
    TokenData,
    UnexpectedLoginUserError,
    VerifyPasswordError,
)
from app.auth.auth_service_validations import (
    validate_jwt_credentials_missing,
    validate_token_exists,
    validate_token_is_expired,
)
from app.exceptions.base_exceptions_schema import BadParameterError
from app.logging.logging_constants import LOGGING_AUTH_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.login.login_schema import InvalidCredentialsLoginError
from app.spotify_electron.user.base_user_schema import (
    BaseUserNotFoundError,
    BaseUserServiceError,
)
from app.spotify_electron.utils.validations.validation_utils import validate_parameter

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 days
DAYS_TO_EXPIRE_COOKIE = 7

auth_service_logger = SpotifyElectronLogger(LOGGING_AUTH_SERVICE).get_logger()


def create_access_token(data: dict[str, str], expires_delta: timedelta | None = None) -> str:
    """Create a jwt token from data with a expire date

    Args:
    ----
        data (dict): Info to be stored in the token
        expires_delta (timedelta | None, optional): Expire date of the token

    Raises:
    ------
        CreateJWTError: if an error ocurred creating JWT Token

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
        to_encode.update({"exp": expire})  # type: ignore
        encoded_jwt = jwt.encode(
            to_encode,
            AuthConfig.SIGNING_SECRET_KEY,
            algorithm=ALGORITHM,
        )
    except Exception as exception:
        raise CreateJWTError from exception
    else:
        auth_service_logger.info(f"JWT created from data: {data}")
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
        BadJWTTokenProvidedError: invalid token provided

    Returns:
    -------
        TokenData: the data provided by the JWT Token

    """
    try:
        validate_token_exists(token_raw_data)
        payload = jwt.decode(
            token_raw_data,
            AuthConfig.SIGNING_SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        username = payload.get("access_token")
        role = payload.get("role")
        token_type = payload.get("token_type")

        credentials = [username, role, token_type]
        validate_jwt_credentials_missing(credentials)
        token_data = TokenData(username=username, role=role, token_type=token_type)  # type: ignore

    except JWTNotProvidedError as exception:
        auth_service_logger.exception("No JWT Token was provided")
        raise BadJWTTokenProvidedError from exception
    except JWTMissingCredentialsError as exception:
        auth_service_logger.exception(
            f"One or more credentials obtained from JWT are missing: {credentials}"
        )
        raise BadJWTTokenProvidedError from exception
    except JWTError as exception:
        auth_service_logger.exception("Error decoding JWT Token")
        raise BadJWTTokenProvidedError from exception
    except Exception as exception:
        auth_service_logger.exception("Unexpected error getting data from JWT Token")
        raise BadJWTTokenProvidedError from exception
    else:
        auth_service_logger.info(f"Token data: {token_data}")
        return token_data


def hash_password(plain_password: str) -> bytes:
    """Hash a password with a randomly-generated salt

    Args:
    ----
        plain_password (str): provided plain password

    Returns:
    -------
        bytes: the hashed password

    """
    encoded_password = plain_password.encode()
    return bcrypt.hashpw(encoded_password, bcrypt.gensalt())


def verify_password(plain_password: str, hashed_password: bytes) -> None:
    """Verifies if plain text password is the same as a hashed password

    Args:
    ----
        plain_password (str): plain text password
        hashed_password (bytes): hashed password

    Raises:
    ------
        VerifyPasswordError: if passwords don't match

    """
    if not bcrypt.checkpw(plain_password.encode(), hashed_password):
        raise VerifyPasswordError


def get_token_expire_date() -> datetime:
    """Returns expire date for new token

    Returns
    -------
        datetime: the expire date for the token

    """
    current_utc_datetime = datetime.now(timezone.utc).replace(tzinfo=timezone.utc)  # noqa: UP017 TODO
    return current_utc_datetime + timedelta(days=DAYS_TO_EXPIRE_COOKIE)


async def login_user(name: str, password: str) -> str:
    """Checks user credentials and return a jwt token

    Args:
    ----
        name (str): Users's name
        password (str): Users's password

    Raises:
    ------
        InvalidCredentialsLoginError: bad user credentials
        VerifyPasswordError: failing authenticating user and password
        BaseUserNotFoundError: user doesn't exists
        UnexpectedLoginUserError: unexpected error during user login

    Returns:
    -------
        str: the JWT Token

    """
    try:
        validate_parameter(name)
        validate_parameter(password)
        await base_user_service_validations.validate_user_should_exists(name)

        user_type = await base_user_service.get_user_type(user_name=name)
        user_password = await base_user_service.get_user_password(user_name=name)

        verify_password(password, user_password)

        jwt_data = {
            "access_token": name,
            "role": user_type.value,
            "token_type": "bearer",
        }
        access_token_data = create_access_token(jwt_data)

    except BadParameterError as exception:
        auth_service_logger.exception("Invalid login credentials")
        raise InvalidCredentialsLoginError from exception
    except VerifyPasswordError as exception:
        auth_service_logger.exception("Passwords Validation failed: passwords don't match")
        raise VerifyPasswordError from exception
    except CreateJWTError as exception:
        auth_service_logger.exception(f"Error creating JWT Token from data: {jwt_data}")
        raise VerifyPasswordError from exception
    except BaseUserNotFoundError as exception:
        auth_service_logger.exception(f"User {name} doesn't exists")
        raise BaseUserNotFoundError from exception
    except BaseUserServiceError as exception:
        auth_service_logger.exception(
            f"Unexpected error in User service while login user: {name}"
        )
        raise UnexpectedLoginUserError from exception
    except Exception as exception:
        auth_service_logger.exception(f"Unexpected error login user: {name}")
        raise UnexpectedLoginUserError from exception
    else:
        auth_service_logger.info(f"User {name} logged successfully")
        return access_token_data


async def login_user_with_token(raw_token: str) -> None:
    """User Login with token

    Args:
        raw_token (str): the jwt token

    Raises:
        JWTValidationError: invalid JWT credentials
        BaseUserNotFoundError: user doesn't exists
        UnexpectedLoginUserError: unexpected error during user login
    """
    try:
        validate_jwt(raw_token)

        token_data = get_jwt_token_data(raw_token)
        await base_user_service_validations.validate_user_should_exists(token_data.username)

    except (JWTValidationError, BadJWTTokenProvidedError) as exception:
        auth_service_logger.exception(f"Error validating jwt token data: {raw_token}")
        raise JWTValidationError from exception
    except BaseUserNotFoundError as exception:
        auth_service_logger.exception(f"User {token_data.username} not found")
        raise BaseUserNotFoundError from exception
    except BaseUserServiceError as exception:
        auth_service_logger.exception(
            f"Unexpected error in User service while auto login user: {token_data.username}"
        )
        raise UnexpectedLoginUserError from exception
    except Exception as exception:
        auth_service_logger.exception(
            f"Unexpected error auto login user: {token_data.username}"
        )
        raise UnexpectedLoginUserError from exception


def validate_jwt(token: str) -> None:
    """Check if JWT token is valid

    Args:
    ----
        token (str): the token to validate

    Raises:
    ------
        JWTValidationError: if the validation was not succesfull

    """
    try:
        decoded_token = jwt.decode(
            token,
            AuthConfig.SIGNING_SECRET_KEY,
            ALGORITHM,
        )
        validate_token_is_expired(decoded_token)

    except JWTError as exception:
        auth_service_logger.exception(f"Error decoding token: {token}")
        raise JWTValidationError from exception

    except JWTExpiredError as exception:
        auth_service_logger.exception(f"Token is expired: {token}")
        raise JWTValidationError from exception

    except Exception as exception:
        auth_service_logger.exception(f"Unexpected error validating token: {token}")
        raise JWTValidationError from exception


def get_authorization_bearer_from_headers(headers: list[tuple[bytes, Any]]) -> str | None:
    """Get authorization bearer value from HTTP header 'authorization'

    Args:
        headers (list[tuple]): headers

    Returns:
        str | None: the authorization value
    """
    for key, value in headers:
        if key == b"authorization":
            return value.decode("utf-8")
    return None
