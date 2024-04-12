from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED

import app.services.security_service as security_service
from app.logging.logger_constants import LOGGIN_CHECK_AUTH_JWT_MIDDLEWARE
from app.logging.logging_schema import SpotifyElectronLogger

check_jwt_auth_middleware_logger = SpotifyElectronLogger(
    LOGGIN_CHECK_AUTH_JWT_MIDDLEWARE
).getLogger()


class CheckJwtAuthMiddleware(BaseHTTPMiddleware):
    """Middleware for authenticating user credentials"""

    bypass_urls = {
        "GET": [
            "/usuarios/whoami",
            "/usuarios/whoami/",
            "/docs",
            "/docs/",
            "/openapi.json",
        ],
        "POST": [
            "/usuarios/",
            "/usuarios",
            "/login/",
            "/login",
            "/artistas/",
            "/artistas",
        ],
    }
    """HTTP Urls that wont be checked"""
    bypass_methods = ["DELETE"]
    """"HTTP Methods that wont be checked"""

    def bypass_request(self, request: Request) -> bool:
        """Returns if the request has to be bypassed or not

        Args:
            request (Request): the incoming request

        Returns:
            bool: if the return has to be bypassed
        """

        check_jwt_auth_middleware_logger.debug(
            f"Request method {request.method}\n \
            Request URL {request.url}\n \
            Request headers {request.headers}"
        )

        if request.method in self.bypass_methods or (
            request.method in self.bypass_urls.keys()
            and request.url.path in self.bypass_urls[request.method]
        ):
            return True
        return False

    async def dispatch(self, request: Request, call_next):
        try:
            if self.bypass_request(request):
                check_jwt_auth_middleware_logger.debug(
                    f"Bypassed request : {request.method} {request.url}"
                )
                response = await call_next(request)
                return response

            jwt = request.headers["authorization"]
            return await self._handle_jwt_validation(jwt, request, call_next)
        except Exception as dispatch_error:
            check_jwt_auth_middleware_logger.error(
                f"Error dispatching request {request} with error : {dispatch_error}"
            )
            return Response(
                content="Invalid Credentials",
                status_code=HTTP_401_UNAUTHORIZED,
            )

    async def _handle_jwt_validation(self, jwt, request, call_next) -> Response:
        """Handles JWT validation, sends HTTP_401_UNAUTHORIZED if jwt is not valid or\
            continues the workflow

        Args:
            jwt (_type_): the jwt token
            request (_type_): the incoming request
            call_next (_type_): the method for continuing the workflow

        Returns:
            Response : the Response thats gonna be sended to the client,\
                HTTP_401_UNAUTHORIZED if jwt is not valid
        """
        if not security_service.check_jwt_is_valid(jwt):
            check_jwt_auth_middleware_logger.error(
                f"Request with invalid JWT {jwt} {request}"
            )
            return Response(
                content="Invalid Credentials", status_code=HTTP_401_UNAUTHORIZED
            )
        response = await call_next(request)
        return response
