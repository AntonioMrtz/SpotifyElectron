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
from app.exceptions.base_exceptions_schema import BadParameterException
from app.logging.logging_constants import LOGGING_AUTH_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.login.login_schema import InvalidCredentialsLoginException
from app.spotify_electron.user.user.user_schema import (
    UserDTO,
    UserNotFoundException,
    UserServiceException,
)
from app.spotify_electron.utils.validations.validation_utils import validate_parameter

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 days
DAYS_TO_EXPIRE_COOKIE = 7

auth_service_logger = SpotifyElectronLogger(LOGGING_AUTH_SERVICE).getLogger()


def create_access_token(data: dict[str, str], expires_delta: timedelta | None = None) -> str:
    """Creates a JWT access token with given data and expiration.

    Args:
       data (dict): Dictionary of data to encode in the token.
       expires_delta (timedelta | None, optional): Optional custom expiration time delta.
       If not provided, default expiration time will be used.

    Raises:
       CreateJWTException: If an error occurs while creating the token.

    Returns:
       str: JWT token string containing the encoded data.
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
        raise CreateJWTException from exception
    else:
        auth_service_logger.info(f"JWT created from data: {data}")
        return encoded_jwt


def get_jwt_token_data(
    token_raw_data: str,
) -> TokenData:
    """Decodes a JWT token and extracts the user data.

    Args:
       token_raw_data (str): Raw JWT token string to decode.

    Raises:
       BadJWTTokenProvidedException: If the token is invalid, missing required data,
           or cannot be decoded.

    Returns:
        TokenData: object containing the decoded user information.
    """
    validate_token_exists(token_raw_data)
    try:
        payload = jwt.decode(
            token_raw_data,  # type: ignore
            AuthConfig.SIGNING_SECRET_KEY,
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
            f"One or more credentials obtained from JWT are missing: {credentials}"
        )
        raise BadJWTTokenProvidedException from exception
    except JWTError as exception:
        auth_service_logger.exception("Error decoding JWT Token")
        raise BadJWTTokenProvidedException from exception
    except Exception as exception:
        auth_service_logger.exception("Unexpected error getting data from JWT Token")
        raise BadJWTTokenProvidedException from exception
    else:
        auth_service_logger.info(f"Token data: {token_data}")
        return token_data


def get_current_user(
    token: TokenData,
) -> UserDTO:
    """Retrieves the current user based on JWT token data.

    Args:
       token (TokenData): TokenData object containing user information.

    Raises:
       UserNotFoundException: If the user from the token does not exist.
       JWTGetUserException: If an error occurs while retrieving the user.

    Returns:
       UserDTO: object for the authenticated user.
    """
    try:
        jwt_username = token.username

        user = base_user_service.get_user(jwt_username)
    except UserNotFoundException as exception:
        auth_service_logger.exception(f"User {jwt_username} not found")
        raise UserNotFoundException from exception
    except Exception as exception:
        auth_service_logger.exception(f"Unexpected exception getting user from token {token}")
        raise JWTGetUserException from exception
    else:
        auth_service_logger.info(f"Get Current User successful: {jwt_username}")
        return user


def hash_password(plain_password: str) -> bytes:
    """Hashes a password using bcrypt with a random salt.

    Args:
       plain_password (str): Password in plaintext to hash.

    Returns:
       bytes: Bytes containing the hashed password.
    """
    return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())


def verify_password(plain_password: str, hashed_password: bytes) -> None:
    """Verifies if a plaintext password matches its hashed version.

    Args:
       plain_password (str): Password in plaintext.
       hashed_password (bytes): Encrypted password bytes to compare against.

    Raises:
       VerifyPasswordException: If the passwords do not match.
    """
    if not bcrypt.checkpw(plain_password.encode(), hashed_password):
        raise VerifyPasswordException


def get_token_expire_date() -> datetime:
    """Calculates the expiration date for a new token.

    Returns:
       datetime: Datetime object representing when the token will expire.
    """
    current_utc_datetime = datetime.now(timezone.utc).replace(tzinfo=timezone.utc)  # noqa: UP017 TODO
    return current_utc_datetime + timedelta(days=DAYS_TO_EXPIRE_COOKIE)


def login_user(name: str, password: str) -> str:
    """Authenticates a user and generates a JWT token.

    Args:
       name (str): Username to authenticate.
       password (str): User's password.

    Returns:
       str: JWT token string for the authenticated user.

    Raises:
       InvalidCredentialsLoginException: If the login credentials are invalid.
       VerifyPasswordException: If password verification fails.
       UserNotFoundException: If the user does not exist.
       UnexpectedLoginUserException: If an unexpected error occurs during login.
    """
    try:
        validate_parameter(name)
        validate_parameter(password)
        base_user_service_validations.validate_user_should_exists(name)

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
        auth_service_logger.exception("Passwords Validation failed: passwords don't match")
        raise VerifyPasswordException from exception
    except CreateJWTException as exception:
        auth_service_logger.exception(f"Error creating JWT Token from data: {jwt_data}")
        raise VerifyPasswordException from exception
    except UserNotFoundException as exception:
        auth_service_logger.exception(f"User {name} doesn't exists")
        raise UserNotFoundException from exception
    except UserServiceException as exception:
        auth_service_logger.exception(
            f"Unexpected error in User service while login user: {name}"
        )
        raise UnexpectedLoginUserException from exception
    except Exception as exception:
        auth_service_logger.exception(f"Unexpected error login user: {name}")
        raise UnexpectedLoginUserException from exception
    else:
        auth_service_logger.info(f"User {name} logged successfully")
        return access_token_data


def login_user_with_token(raw_token: str) -> None:
    """User Login with token

    Args:
        raw_token (str): the JWT token

    Raises:
        JWTValidationException: invalid JWT credentials
        UserNotFoundException: user doesn't exists
        UnexpectedLoginUserException: unexpected error during user login
    """
    try:
        validate_jwt(raw_token)

        token_data = get_jwt_token_data(raw_token)
        base_user_service_validations.validate_user_should_exists(token_data.username)

    except (JWTValidationException, BadJWTTokenProvidedException) as exception:
        auth_service_logger.exception(f"Error validating jwt token data: {raw_token}")
        raise JWTValidationException from exception
    except UserNotFoundException as exception:
        auth_service_logger.exception(f"User {token_data.username} not found")
        raise UserNotFoundException from exception
    except UserServiceException as exception:
        auth_service_logger.exception(
            f"Unexpected error in User service while auto login user: {token_data.username}"
        )
        raise UnexpectedLoginUserException from exception
    except Exception as exception:
        auth_service_logger.exception(
            f"Unexpected error auto login user: {token_data.username}"
        )
        raise UnexpectedLoginUserException from exception


def validate_jwt(token: str) -> None:
    """Validates a JWT token's authenticity and expiration.

    Args:
       token (str): The JWT token string to validate.

    Raises:
       JWTValidationException: If the token is invalid, expired, or validation fails.
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
        raise JWTValidationException from exception

    except JWTExpiredException as exception:
        auth_service_logger.exception(f"Token is expired: {token}")
        raise JWTValidationException from exception

    except Exception as exception:
        auth_service_logger.exception(f"Unexpected error validating token: {token}")
        raise JWTValidationException from exception


def validate_jwt_user_matches_user(token: TokenData, user_name: str) -> None:
    """Validates that the token belongs to the specified user.

    Args:
       token (TokenData): JWT token containing user data.
       user_name (str): Username to validate against token.

    Raises:
       UserUnauthorizedException: If the username doesn't match the token's user.
    """
    if not token.username == user_name:
        raise UserUnauthorizedException


def validate_token_is_expired(token: dict[str, Any]) -> None:
    """Validates that a JWT token has not expired.

    Args:
       token (dict): The token to validate.

    Raises:
       JWTExpiredException: If the token expiration date has passed.
    """
    expiration_time = datetime.fromtimestamp(token["exp"], timezone.utc)  # noqa: UP017 TODO
    if expiration_time < datetime.now(timezone.utc):  # noqa: UP017 TODO
        raise JWTExpiredException


def validate_token_exists(token: Any) -> None:
    """Validates that a JWT token exists.

    Args:
       token (Any): The token to validate.

    Raises:
       JWTNotProvidedException: If the token is None.
    """
    if token is None:
        raise JWTNotProvidedException


def validate_jwt_credentials_missing(credentials: list[Any]) -> None:
    """Validates that all JWT credentials are present.

    Args:
       credentials (list[str]): List of credentials to validate.

    Raises:
       JWTMissingCredentialsException: If any credential is missing.
    """
    for credential in credentials:
        if credential is None:
            raise JWTMissingCredentialsException
