"""
Validations for Common user repositories
"""

from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from app.spotify_electron.user.base_user_schema import (
    BaseUserCreateException,
    BaseUserDAO,
    BaseUserDeleteException,
    BaseUserGetPasswordException,
    BaseUserNotFoundException,
    BaseUserUpdateException,
)


def validate_password_exists(password: bytes) -> None:
    """Raises an exception if cant get password from user

    Args:
        password (bytes): user password

    Raises:
        BaseUserGetPasswordException: if there's no password retrieved
    """
    if not password:
        raise BaseUserGetPasswordException


def validate_user_exists(user: BaseUserDAO | None) -> None:
    """Raises an exception if user doesn't exists

    Args:
    ----
        user (BaseUserDAO | None): the user

    Raises:
    ------
        BaseUserNotFoundException: if the user doesn't exists

    """
    if user is None:
        raise BaseUserNotFoundException


def validate_user_update(result: UpdateResult) -> None:
    """Raises an exception if user update was not done

    Args:
        result (UpdateResult): update result

    Raises:
        BaseUserUpdateException: if the update was not done
    """
    if not result.acknowledged:
        raise BaseUserUpdateException


def validate_user_delete_count(result: DeleteResult) -> None:
    """Raises an exception if user deletion count was 0

    Args:
    ----
        result (DeleteResult): the result from the deletion

    Raises:
    ------
        BaseUserDeleteException: if the deletion was not done

    """
    if result.deleted_count == 0:
        raise BaseUserDeleteException


def validate_user_create(result: InsertOneResult) -> None:
    """Raises an exception if user insertion was not done

    Args:
    ----
        result (InsertOneResult): the result from the insertior

    Raises:
    ------
        BaseUserCreateException: if the insetion was not done

    """
    if not result.acknowledged:
        raise BaseUserCreateException
