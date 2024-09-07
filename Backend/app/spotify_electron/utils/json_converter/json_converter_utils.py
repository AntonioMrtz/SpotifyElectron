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
    """Returns json string from an object

    Args:
    ----
        object (Any): the object that's going to be converted into json string

    Raises:
    ------
        JsonEncodeException: if an error occurred while encoding the object \
            into json string

    Returns:
    -------
        str: the object converted into json string

    """
    return _get_json_from_model(object)


def get_json_with_iterable_field_from_model(object: Any, field_name: str) -> str:
    """Returns a json string that contains an object inside a field name

    Args:
    ----
        object (Any): the object to be put inside a field name
        field_name (str): the name of the field name where the object will be put on

    Returns:
    -------
        str: the json string with the object inside a field name

    """
    object_dict = {field_name: object}
    return _get_json_from_model(object_dict)


def _get_json_from_model(object: Any) -> str:
    """Returns json string from an object

    Args:
    ----
        object (Any): the object that's going to be converted into json string

    Raises:
    ------
        JsonEncodeException: if an error occurred while encoding the object \
            into json string

    Returns:
    -------
        str: the object converted into json string

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
