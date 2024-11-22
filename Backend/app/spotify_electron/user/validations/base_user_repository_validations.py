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
    """Validates that a user exists.

    Args:
       user (UserDAO | None): The user to validate.

    Raises:
       UserNotFoundException: If the user is None.
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
    """Validates that a user was successfully deleted.

    Args:
       result (DeleteResult): Result from the database deletion operation.

    Raises:
       UserDeleteException: If no user was deleted.
    """
    if result.deleted_count == 0:
        raise UserDeleteException


def validate_user_create(result: InsertOneResult) -> None:
    """Validates that a user was successfully created.

    Args:
       result (InsertOneResult): Result from the database insertion operation.

    Raises:
       UserCreateException: If the user insertion was not acknowledged.
    """
    if not result.acknowledged:
        raise UserCreateException
