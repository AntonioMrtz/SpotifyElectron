import json
from dataclasses import dataclass

from app.exceptions.exceptions_schema import SpotifyElectronException
from app.model.UserType import User_Type


@dataclass
class TokenData:
    username: str
    role: User_Type
    token_type: str

    def get_json(self) -> str:
        return json.dumps(self.__dict__)


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
