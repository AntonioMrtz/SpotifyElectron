"""
Validations for Auth service
"""

from datetime import datetime, timezone
from typing import Any

from app.auth.auth_schema import (
    JWTExpiredError,
    JWTMissingCredentialsError,
    JWTNotProvidedError,
    TokenData,
    UserUnauthorizedError,
)


def validate_jwt_user_matches_user(token: TokenData, user_name: str) -> None:
    """Validates if user matches the jwt user

    Args:
        token (TokenData): jwt token
        user_name (str): user

    Raises:
        UserUnauthorizedError: if the user didn't match the jwt user
    """
    if not token.username == user_name:
        raise UserUnauthorizedError


def validate_token_is_expired(token: dict[str, Any]) -> None:
    """Checks if token is expired comparing current date with expiration date

    Args:
        token (dict[str, Any]): token to check

    Raises:
        JWTExpiredError: token is expired
    """
    expiration_time = datetime.fromtimestamp(token["exp"], timezone.utc)  # noqa: UP017 TODO
    if expiration_time < datetime.now(timezone.utc):  # noqa: UP017 TODO
        raise JWTExpiredError


def validate_token_exists(token: Any) -> None:
    """Check whether jwt token is None or not

    Args:
        token (Any): the incoming token

    Raises:
        JWTNotProvidedError: if the token is None
    """
    if token is None:
        raise JWTNotProvidedError


def validate_jwt_credentials_missing(credentials: list[Any]) -> None:
    """Check if any jwt credentials are missing

    Args:
        credentials (list[Any]): list with the obtained credentials

    Raises:
        JWTMissingCredentialsError: if a credential is missing
    """
    for credential in credentials:
        if credential is None:
            raise JWTMissingCredentialsError
