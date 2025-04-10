"""
Validations for artist repository
"""

import app.spotify_electron.user.artist.artist_service as artist_service
from app.auth.auth_schema import UserUnauthorizedError
from app.spotify_electron.user.artist.artist_schema import ArtistAlreadyExistsError


async def validate_user_should_be_artist(user_name: str) -> None:
    """Validates if user is artist

    Args:
        user_name (str): the user name

    Raises:
        UserUnauthorizedError: if the user is not artist
    """
    does_artist_exist = await artist_service.does_artist_exists(user_name)
    if not does_artist_exist:
        raise UserUnauthorizedError


async def validate_artist_should_not_exist(user_name: str) -> None:
    """Validate that artist should not exist

    Args:
        user_name (str): the artist's user name

    Raises:
        ArtistAlreadyExistsError: if artist already exists
    """
    does_artist_exist = await artist_service.does_artist_exists(user_name)
    if does_artist_exist:
        raise ArtistAlreadyExistsError
