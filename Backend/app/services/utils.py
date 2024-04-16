from typing import Any

from app.exceptions.exceptions_schema import BadParameterException


def checkValidParameterString(parameter: Any) -> bool:
    """Checks if the parameter string is not None or empty"""
    if parameter is None or parameter == "":
        raise BadParameterException(parameter)

    return True
