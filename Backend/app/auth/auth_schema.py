"""
Authentication schema for domain model
"""

import binascii
import os
from dataclasses import dataclass

from app.exceptions.base_exceptions_schema import SpotifyElectronException
from app.spotify_electron.user.user.user_schema import UserType

TOKEN_HEADER_FIELD_NAME = "Authorization"
BEARER_SCHEME_NAME = "Bearer"
JWT_COOKIE_HEADER_FIELD_NAME = "jwt"


@dataclass
class TokenData:
    """Class that contains Auth token info"""

    username: str
    role: UserType
    token_type: str


class FakeRequest:
    """Fake Request Object for bypassing authentication token HTTP incoming format"""

    headers: dict[str, str] = {}

    def __init__(self, auth_value: str) -> None:
        self.headers[TOKEN_HEADER_FIELD_NAME] = auth_value


class AuthConfig:
    """Stores application authentication config"""

    VERTIFICATION_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DAYS_TO_EXPIRE_COOKIE: int
    SIGNING_SECRET_KEY: str
    """Key for signing JWT, generated using `openssl rand -hex 16`"""

    @classmethod
    def init_auth_config(
        cls,
        verification_algorithm: str,
        access_token_expire_minutes: int,
        days_to_expire_cookie: int,
    ) -> None:
        """Init authentication configuration, required to start the app successfully

        Args:
            verification_algorithm (str): JWT verification algorithm
            access_token_expire_minutes (int): minutes until the JWT expires
            days_to_expire_cookie (int): days until cookies expire
        """
        random_bytes = os.urandom(16)
        hex_string = binascii.hexlify(random_bytes).decode("utf-8")
        cls.SIGNING_SECRET_KEY = hex_string

        cls.VERTIFICATION_ALGORITHM = verification_algorithm
        cls.ACCESS_TOKEN_EXPIRE_MINUTES = access_token_expire_minutes
        cls.DAYS_TO_EXPIRE_COOKIE = days_to_expire_cookie


class BadJWTTokenProvidedException(SpotifyElectronException):
    """Bad JWT Token provided"""

    ERROR = "bad JWT Token provided"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTNotProvidedException(SpotifyElectronException):
    """JWT Token not provided"""

    ERROR = "JWT Token not provided"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTMissingCredentialsException(SpotifyElectronException):
    """Missing credentials obtained from JWT Token"""

    ERROR = "Missing credentials in JWT Token"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTGetUserException(SpotifyElectronException):
    """Get user data from JWT Token error"""

    ERROR = "Error getting user data from JWT Token"

    def __init__(self):
        super().__init__(self.ERROR)


class CreateJWTException(SpotifyElectronException):
    """JWT Token creation error"""

    ERROR = "Error creating JWT Token"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTDecodeException(SpotifyElectronException):
    """Decoding JWT Token error"""

    ERROR = "Error decoding JWT Token"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTExpiredException(SpotifyElectronException):
    """Expired JWT Token"""

    ERROR = "JWT token is expired"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTValidationException(SpotifyElectronException):
    """Validating JWT Token error"""

    ERROR = "JWT Token validation failure"

    def __init__(self):
        super().__init__(self.ERROR)


class VerifyPasswordException(SpotifyElectronException):
    """Validating password error"""

    ERROR = "Password validation failure"

    def __init__(self):
        super().__init__(self.ERROR)


class UnexpectedGetJWTTokenException(SpotifyElectronException):
    """Unexpected error getting JWT token data"""

    ERROR = "Unexpected error getting data from JWT"

    def __init__(self):
        super().__init__(self.ERROR)


class UnexpectedLoginUserException(SpotifyElectronException):
    """Unexpected error during user login"""

    ERROR = "Unexpected error during user login"

    def __init__(self):
        super().__init__(self.ERROR)


class UserUnauthorizedException(SpotifyElectronException):
    """User is unauthorized to access the resource"""

    def __init__(self):
        super().__init__("User is unauthorized to access the resource")
