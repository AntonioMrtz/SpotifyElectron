from typing import Any

from app.exceptions.base_exceptions_schema import BadParameterException


def validate_parameter(parameter: Any):
    """Checks if the parameter string is not None or empty"""
    if parameter is None or parameter == "":
        raise BadParameterException(parameter)
