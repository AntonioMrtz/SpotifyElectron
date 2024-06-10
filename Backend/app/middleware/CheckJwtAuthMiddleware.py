"""Middleware for authenticate incoming HTTP Requests using JWT Token"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED

import app.spotify_electron.security.security_service as security_service
from app.logging.logging_constants import LOGGIN_CHECK_AUTH_JWT_MIDDLEWARE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.security.security_schema import JWTValidationException

check_jwt_auth_middleware_logger = SpotifyElectronLogger(
    LOGGIN_CHECK_AUTH_JWT_MIDDLEWARE
).getLogger()


class CheckJwtAuthMiddleware(BaseHTTPMiddleware):
    """Middleware for authenticating user credentials"""

    bypass_urls = {
        "GET": [
            "/users/whoami",
            "/users/whoami/",
            "/docs",
            "/docs/",
            "/openapi.json",
            "/health/",
        ],
        "POST": [
            "/users/",
            "/users",
            "/login/",
            "/login",
            "/artists/",
            "/artists",
            "/token",
        ],
    }
    """HTTP Urls that wont be checked"""
    bypass_methods = ["DELETE"]
    """"HTTP Methods that wont be checked"""

    def bypass_request(self, request: Request) -> bool:
        """Returns if the request has to be bypassed or not

        Args:
        ----
            request (Request): the incoming request

        Returns:
        -------
            bool: if the return has to be bypassed

        """
        check_jwt_auth_middleware_logger.debug(
            f"Request method {request.method}\n Request URL {request.url}\n"
        )

        if request.method in self.bypass_methods or (
            request.method in self.bypass_urls
            and request.url.path in self.bypass_urls[request.method]
        ):
            return True
        return False

    async def dispatch(self, request: Request, call_next):
        """Manages the incoming HTTP request and decides wheter or not it has to be blocked

        Args:
            request (Request): the incoming request
            call_next (_type_): the method to call next

        Returns:
            _type_: the call next output if request was not blocked
        """
        try:
            if self.bypass_request(request):
                check_jwt_auth_middleware_logger.debug(
                    f"Bypassed request : {request.method} {request.url}"
                )
                return await call_next(request)

            jwt = request.headers["authorization"]
            return await self._handle_jwt_validation(jwt, request, call_next)
        except Exception:
            return Response(
                content="Invalid Credentials",
                status_code=HTTP_401_UNAUTHORIZED,
            )

    async def _handle_jwt_validation(
        self, jwt: str, request: Request, call_next
    ) -> Response:
        """Handles JWT validation, sends HTTP_401_UNAUTHORIZED if jwt is not valid or\
            continues the workflow

        Args:
        ----
            jwt (str): the jwt token
            request (Request): the incoming request
            call_next (_type_): the method for continuing the workflow

        Returns:
        -------
            Response: the Response thats gonna be sended to the client,\
                HTTP_401_UNAUTHORIZED if jwt is not valid

        """
        try:
            security_service.validate_jwt(jwt)
        except (JWTValidationException, Exception):
            check_jwt_auth_middleware_logger.exception(
                f"Request with invalid JWT {jwt} {request}"
            )
            return Response(
                content="Invalid Credentials", status_code=HTTP_401_UNAUTHORIZED
            )
        else:
            return await call_next(request)
