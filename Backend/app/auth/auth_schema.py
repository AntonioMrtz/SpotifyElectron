"""Authentication schema for domain model"""

from dataclasses import dataclass

from app.exceptions.base_exceptions_schema import SpotifyElectronError
from app.logging.logging_constants import LOGGING_AUTH_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
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
    """Fake Request Object for bypassing authentication token HTTP incoming format
    TODO this must go with https://trello.com/c/rSvoOwPn/452-jwt-auth-backend-performance-improvements
    """

    headers: dict[str, str] = {}

    def __init__(self, auth_value: str) -> None:
        self.headers[TOKEN_HEADER_FIELD_NAME] = auth_value


class AuthConfig:
    """Stores application authentication config"""

    VERIFICATION_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DAYS_TO_EXPIRE_COOKIE: int
    SIGNING_SECRET_KEY: str
    """Key for signing JWT, generated using `openssl rand -hex 16`"""

    @classmethod
    def init_auth_config(
        cls,
        verification_algorithm: str,
        secret_key_sign: str,
        access_token_expire_minutes: int,
        days_to_expire_cookie: int,
    ) -> None:
        """Init authentication configuration, required to start the app successfully

        Args:
            verification_algorithm: JWT verification algorithm
            secret_key_sign: 32 byte key(16 characters) for signing JWT Tokens that\
                  will authenticate the user
            access_token_expire_minutes: minutes until the JWT expires
            days_to_expire_cookie: days until cookies expire
        """
        cls.logger = SpotifyElectronLogger(LOGGING_AUTH_SERVICE).get_logger()
        cls.SIGNING_SECRET_KEY = secret_key_sign
        cls.VERIFICATION_ALGORITHM = verification_algorithm
        cls.ACCESS_TOKEN_EXPIRE_MINUTES = access_token_expire_minutes
        cls.DAYS_TO_EXPIRE_COOKIE = days_to_expire_cookie
        cls.check_auth_health()

    @classmethod
    def check_auth_health(cls) -> None:
        """Check if the Auth configuration is initialized and functioning.

        Raises:
            AuthServiceHealthCheckError: If the Auth configuration is not properly initialized.
        """
        if (
            not hasattr(cls, "ACCESS_TOKEN_EXPIRE_MINUTES")
            or not hasattr(cls, "DAYS_TO_EXPIRE_COOKIE")
            or not hasattr(cls, "VERIFICATION_ALGORITHM")
            or not hasattr(cls, "SIGNING_SECRET_KEY")
        ):
            raise AuthServiceHealthCheckError
        cls.logger.info("Auth configuration health check successful")


class BadJWTTokenProvidedError(SpotifyElectronError):
    """Bad JWT Token provided"""

    ERROR = "bad JWT Token provided"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTNotProvidedError(SpotifyElectronError):
    """JWT Token not provided"""

    ERROR = "JWT Token not provided"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTMissingCredentialsError(SpotifyElectronError):
    """Missing credentials obtained from JWT Token"""

    ERROR = "Missing credentials in JWT Token"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTGetUserError(SpotifyElectronError):
    """Get user data from JWT Token error"""

    ERROR = "Error getting user data from JWT Token"

    def __init__(self):
        super().__init__(self.ERROR)


class CreateJWTError(SpotifyElectronError):
    """JWT Token creation error"""

    ERROR = "Error creating JWT Token"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTDecodeError(SpotifyElectronError):
    """Decoding JWT Token error"""

    ERROR = "Error decoding JWT Token"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTExpiredError(SpotifyElectronError):
    """Expired JWT Token"""

    ERROR = "JWT token is expired"

    def __init__(self):
        super().__init__(self.ERROR)


class JWTValidationError(SpotifyElectronError):
    """Validating JWT Token error"""

    ERROR = "JWT Token validation failure"

    def __init__(self):
        super().__init__(self.ERROR)


class VerifyPasswordError(SpotifyElectronError):
    """Validating password error"""

    ERROR = "Password validation failure"

    def __init__(self):
        super().__init__(self.ERROR)


class UnexpectedGetJWTTokenError(SpotifyElectronError):
    """Unexpected error getting JWT token data"""

    ERROR = "Unexpected error getting data from JWT"

    def __init__(self):
        super().__init__(self.ERROR)


class UnexpectedLoginUserError(SpotifyElectronError):
    """Unexpected error during user login"""

    ERROR = "Unexpected error during user login"

    def __init__(self):
        super().__init__(self.ERROR)


class UserUnauthorizedError(SpotifyElectronError):
    """User is unauthorized to access the resource"""

    def __init__(self):
        super().__init__("User is unauthorized to access the resource")


class AuthServiceHealthCheckError(SpotifyElectronError):
    """Auth service health check failure"""

    ERROR = "Auth service health check failed"

    def __init__(self):
        super().__init__(self.ERROR)
