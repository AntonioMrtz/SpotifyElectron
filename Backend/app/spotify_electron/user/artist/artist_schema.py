"""Artist schema for User domain model"""

from dataclasses import dataclass
from typing import Any

from app.spotify_electron.user.base_user_schema import (
    BaseUserAlreadyExistsError,
    BaseUserBadNameError,
    BaseUserBadParametersError,
    BaseUserGetPasswordError,
    BaseUserNotFoundError,
    BaseUserRepositoryError,
    BaseUserServiceError,
)
from app.spotify_electron.user.user.user_schema import UserDAO, UserDTO


@dataclass
class ArtistDAO(UserDAO):
    """Represents artist data in the persistence layer"""

    uploaded_songs: list[str]
    total_streams: int = 0


@dataclass
class ArtistDTO(UserDTO):
    """Represents artist data in the endpoints transfer layer"""

    uploaded_songs: list[str]
    total_streams: int = 0


def get_artist_dao_from_document(document: dict[str, Any]) -> ArtistDAO:
    """Get ArtistDAO from document

    Args:
    ----
        document: user document

    Returns:
    -------
        ArtistDAO Object
    """
    return ArtistDAO(
        name=document["name"],
        photo=document["photo"],
        register_date=document["register_date"][:-1],
        password=document["password"],
        playback_history=document["playback_history"],
        playlists=document["playlists"],
        saved_playlists=document["saved_playlists"],
        uploaded_songs=document["uploaded_songs"],
    )


def get_artist_dto_from_dao(artist_dao: ArtistDAO) -> ArtistDTO:
    """Get ArtistDTO from ArtistDAO

    Args:
    ----
        artist_dao: ArtistDAO object

    Returns:
    -------
        ArtistDTO object
    """
    return ArtistDTO(
        name=artist_dao.name,
        photo=artist_dao.photo,
        playback_history=artist_dao.playback_history,
        playlists=artist_dao.playlists,
        register_date=artist_dao.register_date,
        saved_playlists=artist_dao.saved_playlists,
        uploaded_songs=artist_dao.uploaded_songs,
        total_streams=artist_dao.total_streams,
    )


class ArtistRepositoryError(BaseUserRepositoryError):
    """Artist Repository Unexpected error"""

    ERROR = "Error accessing Artist REPOSITORY"

    def __init__(self, error: str = ERROR):
        super().__init__(error)


class ArtistNotFoundError(BaseUserNotFoundError):
    """Artist not found"""

    ERROR = "Artist not found"

    def __init__(self, error: str = ERROR):
        super().__init__(error)


class ArtistBadNameError(BaseUserBadNameError):
    """Bad name for artist"""

    ERROR = "Bad parameters provided for artist"

    def __init__(self, error: str = ERROR):
        super().__init__(error)


class ArtistAlreadyExistsError(BaseUserAlreadyExistsError):
    """Exception raised when an Artist already exists"""

    ERROR = "Artist already exists"

    def __init__(self, error: str = ERROR):
        super().__init__(error)


class ArtistGetPasswordError(BaseUserGetPasswordError):
    """Exception raised when there is an error getting artist password"""

    ERROR = "Error getting Artist password"

    def __init__(self, error: str = ERROR):
        super().__init__(error)


class ArtistServiceError(BaseUserServiceError):
    """Exception raised when there is an unexpected error in artist service"""

    ERROR = "Error accessing Artist Service"

    def __init__(self, error: str = ERROR):
        super().__init__(error)


class ArtistBadParametersError(BaseUserBadParametersError):
    """Exception raised when bad parameters are provided for an Artist"""

    ERROR = "Bad parameters provided for Artist"

    def __init__(self, error: str = ERROR):
        super().__init__(error)
