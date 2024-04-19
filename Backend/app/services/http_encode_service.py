import json
from typing import Any

from fastapi.encoders import jsonable_encoder

from app.exceptions.http_encode_exceptions import JsonEncodeException
from app.logging.http_encode_logging_constants import ENCODING_ERROR
from app.logging.logger_constants import LOGGING_HTTP_ENCODE_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger

http_encode_service_logger = SpotifyElectronLogger(
    LOGGING_HTTP_ENCODE_SERVICE
).getLogger()


def get_json(object: Any) -> str:
    """Returns json string from an object

    Args:
        object (Any): the object thats going to be converted into json string

    Raises:
        JsonEncodeException: if an error occurred while encoding the object \
            into json string

    Returns:
        str: the object converted into json string
    """

    return object_to_json(object)


def get_json_with_iterable_field(object: Any, field_name: str) -> str:
    """Returns json string from an object inside an object with a field name

    Args:
        object (Any): the object thats going to be converted into json string
        field_name (str): the name of the field that will contain the object\
              in the dictionary

    Raises:
        JsonEncodeException: if an error occurred while encoding the object \
            into json string

    Returns:
        str: the object converted into json string inside an object with a field name
    """

    object_dict = {field_name: object}
    return object_to_json(object_dict)


def object_to_json(object: Any) -> str:
    """Returns json string from an object

    Args:
        object (Any): the object thats going to be converted into json string

    Raises:
        JsonEncodeException: if an error occurred while encoding the object \
            into json string

    Returns:
        str: the object converted into json string
    """
    try:
        jsonable_object = jsonable_encoder(object)
        json_object = json.dumps(jsonable_object)
        http_encode_service_logger.debug(
            f"Success encoding object into json : {json_object}"
        )
        return json_object
    except Exception as error:
        http_encode_service_logger.error(f"{ENCODING_ERROR}: {error}")
        raise JsonEncodeException()
