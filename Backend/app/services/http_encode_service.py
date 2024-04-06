import json
from typing import Any

from fastapi.encoders import jsonable_encoder

from app.exceptions.exceptions_schema import SpotifyElectronException
from app.logging.logger_constants import LOGGING_HTTP_ENCODE_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger


http_encode_service = SpotifyElectronLogger(LOGGING_HTTP_ENCODE_SERVICE).getLogger()


def get_json(object: Any) -> str:
    """Returns json string from an object

    Args:
        object (Any): the object thats going to be converted into json string

    Raises:
        JsonEncodeException: if an error ocurred while encoding the object \
            into json string

    Returns:
        str: the object converted into json string
    """
    try:
        return object_to_json(object)
    except JsonEncodeException:
        raise


def get_json_with_iterable_field(object: Any, field_name: str) -> str:
    """Returns json string from an object inside an object with a field name

    Args:
        object (Any): the object thats going to be converted into json string
        field_name (str): the name of the field that will contain the object\
              in the dictionary

    Raises:
        JsonEncodeException: if an error ocurred while encoding the object \
            into json string

    Returns:
        str: the object converted into json string inside an object with a field name
    """

    try:
        object_dict = {field_name: object}
        return object_to_json(object_dict)
    except JsonEncodeException:
        raise


def object_to_json(object: Any) -> str:
    """Returns json string from an object

    Args:
        object (Any): the object thats going to be converted into json string

    Raises:
        JsonEncodeException: if an error ocurred while encoding the object \
            into json string

    Returns:
        str: the object converted into json string
    """
    try:
        jsonable_object = jsonable_encoder(object)
        json_object = json.dumps(jsonable_object)
        http_encode_service.debug(f"Success encoding object into json : {json_object}")
        return json_object
    except Exception as error:
        http_encode_service.critical(f"Error encoding object into json: {error}")
        raise JsonEncodeException()


class JsonEncodeException(SpotifyElectronException):
    """TODO"""

    ENCODED_JSON_ERROR = "Error encoding object into json"

    def __init__(self):
        super().__init__(self.ENCODED_JSON_ERROR)
