from app.exceptions.base_exceptions_schema import BadParameterException
from app.spotify_electron.user.user.user_schema import UserBadNameException
from app.spotify_electron.utils.validations.validation_utils import validate_parameter


def validate_user_name_parameter(name: str) -> None:
    """Raises an exception if name parameter is invalid

    Args:
    ----
        name (str): name

    Raises:
    ------
        UserBadNameException: if name parameter is invalid

    """
    try:
        validate_parameter(name)
    except BadParameterException:
        raise UserBadNameException from BadParameterException
