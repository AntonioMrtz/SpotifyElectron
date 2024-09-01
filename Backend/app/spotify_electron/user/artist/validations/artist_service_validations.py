"""
Validations for artist repository
"""

import app.spotify_electron.user.artist.artist_service as artist_service
from app.auth.auth_schema import UserUnauthorizedException


def validate_user_should_be_artist(user_name: str) -> None:
    """Validate if user is artist

    Args:
        user_name (str): the user name

    Raises:
        UserUnauthorizedException: if the user is not artist
    """
    if not artist_service.does_artist_exists(user_name):
        raise UserUnauthorizedException
