"""JWT Token authentication and injection for endpoints"""

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import app.auth.auth_service as auth_service
from app.auth.auth_schema import (
    BEARER_SCHEME_NAME,
    JWT_COOKIE_HEADER_FIELD_NAME,
    BadJWTTokenProvidedError,
    FakeRequest,
    JWTValidationError,
    TokenData,
)
from app.auth.auth_service import get_authorization_bearer_from_headers, get_jwt_token_data
from app.logging.logging_constants import LOGGING_JWT_BEARER_AUTH
from app.logging.logging_schema import SpotifyElectronLogger

jwt_bearer_logger = SpotifyElectronLogger(LOGGING_JWT_BEARER_AUTH).get_logger()


class JWTBearer(HTTPBearer):
    """JWT Bearer authentication manager"""

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> TokenData:
        """Returns Token data or 403 Code if credentials are invalid

        Args:
            request (Request): the incoming request

        Raises:
            BadJWTTokenProvidedError: invalid credentials

        Returns:
            TokenData: the token data
        """
        # TODO Receiving b'"bearer eyJhbGciOiJIUzI"' from frontend
        # instead of b'bearer eyJhbGciOiJIUzI'
        # replacing " with white space for all headers can be deleted if it's solved
        if len(request.cookies) == 0 or not request.cookies.get(JWT_COOKIE_HEADER_FIELD_NAME):
            jwt_bearer_logger.warning(
                f"Request with no cookies {request}, getting JWT from Authentication Header"
            )
            jwt_raw = get_authorization_bearer_from_headers(request.headers.raw)
        else:
            jwt_raw = request.cookies.get(JWT_COOKIE_HEADER_FIELD_NAME)

        fake_request = FakeRequest(jwt_raw)  # type: ignore
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(  # noqa: UP008
            fake_request  # type: ignore
        )
        if not credentials or credentials.scheme != BEARER_SCHEME_NAME:
            raise BadJWTTokenProvidedError
        try:
            jwt_raw = credentials.credentials
            auth_service.validate_jwt(jwt_raw)
            jwt_token_data = get_jwt_token_data(credentials.credentials)
        except (JWTValidationError, Exception) as exception:
            jwt_bearer_logger.exception(f"Request with invalid JWT {jwt_raw} {request}")
            raise BadJWTTokenProvidedError from exception
        else:
            return jwt_token_data
