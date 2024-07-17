"""
Authentication schema for domain model
"""

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


class BadJWTTokenProvidedException(SpotifyElectronException):
    """Exception for bad JWT Token provided"""

    ERROR = "Exception for bad JWT Token provided"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTNotProvidedException(SpotifyElectronException):
    """Exception for JWT Token not provided"""

    ERROR = "JWT Token not provided"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTMissingCredentialsException(SpotifyElectronException):
    """Exception for missing credentials obtained from JWT Token"""

    ERROR = "Missing credentials in JWT Token"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTGetUserException(SpotifyElectronException):
    """Exception for error getting user data from JWT Token"""

    ERROR = "Error getting user data from JWT Token"

    def __init__(self):
        super().__init__(self.ERROR)


class CreateJWTException(SpotifyElectronException):
    """Exception for error creating JWT Token"""

    ERROR = "Error creating JWT Token"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTDecodeException(SpotifyElectronException):
    """Exception for error decoding JWT Token"""

    ERROR = "Error decoding JWT Token"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTExpiredException(SpotifyElectronException):
    """Exception for expired JWT Token"""

    ERROR = "JWT token is expired"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTValidationException(SpotifyElectronException):
    """Exception for error validating JWT Token"""

    ERROR = "JWT Token validation failure"

    def __init__(self):
        super().__init__(self.ERROR)


class VerifyPasswordException(SpotifyElectronException):
    """Exception for error validating password"""

    ERROR = "Password validation failure"

    def __init__(self):
        super().__init__(self.ERROR)


class UnexpectedGetJWTTokenException(SpotifyElectronException):
    """Exception for unexpected error getting JWT token data"""

    ERROR = "Unexpected error getting data from JWT"

    def __init__(self):
        super().__init__(self.ERROR)


class UnexpectedLoginUserException(SpotifyElectronException):
    """Exception for unexpected error during user login"""

    ERROR = "Unexpected error during user login"

    def __init__(self):
        super().__init__(self.ERROR)


class UserUnauthorizedException(SpotifyElectronException):
    """Exception raised when user is unauthorized to access the resource"""

    def __init__(self):
        super().__init__("User is unauthorized to access the resource")
