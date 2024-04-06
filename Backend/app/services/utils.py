from typing import Any

from app.exceptions.services_exceptions import BadParameterException


def checkValidParameterString(parameter: Any) -> bool:
    """Checks if the parameter string is not None or empty"""
    if parameter is None or parameter == "":
        raise BadParameterException(parameter)

    return True
