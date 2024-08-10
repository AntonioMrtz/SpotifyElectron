"""
Validations for Common user repositories
"""

from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from app.spotify_electron.user.user.user_schema import (
    UserCreateException,
    UserDAO,
    UserDeleteException,
    UserGetPasswordException,
    UserNotFoundException,
    UserUpdateException,
)


def validate_password_exists(password: bytes) -> None:
    """Raises an exception if cant get password from user

    Args:
        password (bytes): user password

    Raises:
        UserGetPasswordException: if there's no password retrieved
    """
    if not password:
        raise UserGetPasswordException


def validate_user_exists(user: UserDAO | None) -> None:
    """Raises an exception if user doesnt exists

    Args:
    ----
        user (UserDAO | None): the user

    Raises:
    ------
        UserNotFoundException: if the user doesnt exists

    """
    if user is None:
        raise UserNotFoundException


def validate_user_update(result: UpdateResult) -> None:
    """Raises an exception if user update was not done

    Args:
        result (UpdateResult): update result

    Raises:
        UserUpdateException: if the update was not done
    """
    if not result.acknowledged:
        raise UserUpdateException


def validate_user_delete_count(result: DeleteResult) -> None:
    """Raises an exception if user deletion count was 0

    Args:
    ----
        result (DeleteResult): the result from the deletion

    Raises:
    ------
        UserDeleteException: if the deletion was not done

    """
    if result.deleted_count == 0:
        raise UserDeleteException


def validate_user_create(result: InsertOneResult) -> None:
    """Raises an exception if user insertion was not done

    Args:
    ----
        result (InsertOneResult): the result from the insertior

    Raises:
    ------
        UserCreateException: if the insetion was not done

    """
    if not result.acknowledged:
        raise UserCreateException
