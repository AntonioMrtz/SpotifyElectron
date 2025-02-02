"""
Validations for Common user repositories
"""

from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from app.spotify_electron.user.base_user_schema import (
    BaseUserCreateError,
    BaseUserDAO,
    BaseUserDeleteError,
    BaseUserGetPasswordError,
    BaseUserNotFoundError,
    BaseUserUpdateError,
)


def validate_password_exists(password: bytes) -> None:
    """Raises an exception if cant get password from user

    Args:
        password (bytes): user password

    Raises:
        BaseUserGetPasswordError: if there's no password retrieved
    """
    if not password:
        raise BaseUserGetPasswordError


def validate_user_exists(user: BaseUserDAO | None) -> None:
    """Raises an exception if user doesn't exists

    Args:
    ----
        user (BaseUserDAO | None): the user

    Raises:
    ------
        BaseUserNotFoundError: if the user doesn't exists

    """
    if user is None:
        raise BaseUserNotFoundError


def validate_user_update(result: UpdateResult) -> None:
    """Raises an exception if user update was not done

    Args:
        result (UpdateResult): update result

    Raises:
        BaseUserUpdateError: if the update was not done
    """
    if not result.acknowledged:
        raise BaseUserUpdateError


def validate_user_delete_count(result: DeleteResult) -> None:
    """Raises an exception if user deletion count was 0

    Args:
    ----
        result (DeleteResult): the result from the deletion

    Raises:
    ------
        BaseUserDeleteError: if the deletion was not done

    """
    if result.deleted_count == 0:
        raise BaseUserDeleteError


def validate_user_create(result: InsertOneResult) -> None:
    """Raises an exception if user insertion was not done

    Args:
    ----
        result (InsertOneResult): the result from the insertior

    Raises:
    ------
        BaseUserCreateError: if the insetion was not done

    """
    if not result.acknowledged:
        raise BaseUserCreateError
