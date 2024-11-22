"""
Json converter utils for building HTTP Json responses from domain objects
"""

import json
from typing import Any

from fastapi.encoders import jsonable_encoder

from app.exceptions.base_exceptions_schema import JsonEncodeException
from app.logging.logging_constants import LOGGING_HTTP_ENCODE_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger

http_encode_service_logger = SpotifyElectronLogger(LOGGING_HTTP_ENCODE_SERVICE).getLogger()


def get_json_from_model(object: Any) -> str:
    """Converts an object to a JSON string.

    Args:
       object (Any): Object to convert to JSON.

    Returns:
       str: JSON string representation of the object.

    Raises:
       JsonEncodeException: If the object cannot be encoded to JSON.
    """
    return _get_json_from_model(object)


def get_json_with_iterable_field_from_model(object: Any, field_name: str) -> str:
    """Converts an object to a JSON string within a named field.

    Args:
       object (Any): Object to convert to JSON.
       field_name: Name of the field to contain the object.

    Returns:
       str: JSON string with the object nested under the field name.
    """
    object_dict = {field_name: object}
    return _get_json_from_model(object_dict)


def _get_json_from_model(object: Any) -> str:
    """Converts an object to a JSON string.

    Args:
       object (Any): Object to convert to JSON.

    Returns:
       str: The JSON string representation of the object.

    Raises:
       JsonEncodeException: If the object cannot be encoded to JSON.
    """
    try:
        jsonable_object = jsonable_encoder(object)
        json_object = json.dumps(jsonable_object)
        http_encode_service_logger.debug(f"Success encoding object into json: {json_object}")
    except Exception:
        http_encode_service_logger.exception(f"Error encoding object {object} into json")
        raise JsonEncodeException()
    else:
        return json_object
