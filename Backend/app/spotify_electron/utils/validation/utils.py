from typing import Any

from app.exceptions.exceptions_schema import BadParameterException


def validate_parameter(parameter: Any) -> bool:
    # TODO , remove boolean return, return None
    """Checks if the parameter string is not None or empty"""
    if parameter is None or parameter == "":
        raise BadParameterException(parameter)

    return True
