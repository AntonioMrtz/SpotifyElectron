"""
Validations for artist repository
"""

import app.spotify_electron.user.artist.artist_service as artist_service
from app.auth.auth_schema import UserUnauthorizedError
from app.spotify_electron.user.artist.artist_schema import ArtistAlreadyExistsError


def validate_user_should_be_artist(user_name: str) -> None:
    """Validate if user is artist

    Args:
        user_name (str): the user name

    Raises:
        UserUnauthorizedError: if the user is not artist
    """
    if not artist_service.does_artist_exists(user_name):
        raise UserUnauthorizedError


def validate_artist_should_not_exist(user_name: str) -> None:
    """Validate if artist already exists

    Args:
        user_name (str): the artist's user name

    Raises:
        ArtistAlreadyExistsError: if artist already exists
    """
    if artist_service.does_artist_exists(user_name):
        raise ArtistAlreadyExistsError
