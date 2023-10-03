from fastapi import Request, Response
from services.security_service import check_jwt_is_valid
from starlette.middleware.base import BaseHTTPMiddleware


class CheckJwtAuth(BaseHTTPMiddleware):

    bypass_urls = {

        "GET": ["/usuarios/whoami", "/usuarios/whoami/", "/docs", "/docs/", "/openapi.json"],
        "POST": ["/usuarios/", "/usuarios", "/login/", "/login", "/artistas/", "/artistas"],
    }

    bypass_methods = ["DELETE"]

    def bypass_request(self, request: Request):
        """ print(request.method)
        print(request.url.path) """

        if request.method in self.bypass_methods:
            return True
        elif request.method in self.bypass_urls.keys() and request.url.path in self.bypass_urls[request.method]:
            return True
        else:
            return False

    async def dispatch(self, request: Request, call_next):
        try:
            if self.bypass_request(request):
                response = await call_next(request)
                return response

            jwt = request.headers["authorization"]
            if check_jwt_is_valid(jwt):
                response = await call_next(request)
                return response
            else:
                return Response(content="Credenciales inválidos", status_code=401)

        except:
            return Response(content="Credenciales inválidos", status_code=401)
