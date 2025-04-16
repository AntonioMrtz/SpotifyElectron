"""Field common validations utils"""

from typing import Any

from app.exceptions.base_exceptions_schema import BadParameterError


def validate_parameter(parameter: Any) -> None:
    """Checks if the parameter string is not None or empty

    Args:
        parameter: parameter name

    Raises:
        BadParameterError: parameter is invalid
    """
    if parameter is None or parameter == "":
        raise BadParameterError(parameter)
