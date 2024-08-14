"""
Field common validations utils
"""

from typing import Any

from app.exceptions.base_exceptions_schema import BadParameterException


def validate_parameter(parameter: Any) -> None:
    """Checks if the parameter string is not None or empty

    Args:
        parameter (Any): parameter name

    Raises:
        BadParameterException: if the parameter is invalid
    """
    if parameter is None or parameter == "":
        raise BadParameterException(parameter)
