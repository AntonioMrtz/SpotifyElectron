"""
Validations for artist repository
"""

from app.auth.security_schema import UserUnauthorizedException
from app.spotify_electron.user.artist.artist_service import does_artist_exists


def validate_user_should_be_artist(user_name: str) -> None:
    """Validate if user is artist

    Args:
        user_name (str): the user name

    Raises:
        UserUnauthorizedException: if the user is not artist
    """
    if not does_artist_exists(user_name):
        raise UserUnauthorizedException
