from fastapi import APIRouter
from fastapi.responses import Response
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

import app.spotify_electron.search.search_service as search_service
import app.spotify_electron.utils.json_converter.json_converter_service as json_converter_service
from app.common.PropertiesMessagesManager import PropertiesMessagesManager
from app.exceptions.exceptions_schema import BadParameterException
from app.exceptions.http_encode_exceptions import JsonEncodeException
from app.logging.logging_constants import LOGGING_SEARCH_CONTROLLER
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.search.search_schema import SearchServiceException

router = APIRouter(
    prefix="/search",
    tags=["search"],
)

search_controller_logger = SpotifyElectronLogger(LOGGING_SEARCH_CONTROLLER).getLogger()


@router.get("/", tags=["search"])
def get_search_nombre(name: str) -> Response:
    """Search for items that partially match name

    Args:
    ----
        name (str): name to match
    """
    try:
        items = search_service.search_by_name(name=name)
        items_json = json_converter_service.get_json_from_model(items)

        return Response(
            items_json, media_type="application/json", status_code=HTTP_200_OK
        )

    except BadParameterException:
        return Response(
            status_code=HTTP_400_BAD_REQUEST,
        )
    except JsonEncodeException:
        search_controller_logger.exception(
            f"{PropertiesMessagesManager.commonEncodingError} : {items}"
        )
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except (Exception, SearchServiceException):
        search_controller_logger.exception(
            PropertiesMessagesManager.commonInternalServerError
        )
        return Response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )