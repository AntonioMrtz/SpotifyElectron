"""
Artist schema for User domain model
"""

from dataclasses import dataclass
from typing import Any

from app.spotify_electron.user.user.user_schema import UserDAO, UserDTO


@dataclass
class ArtistDAO(UserDAO):
    """Represents artist data in the persistence layer"""

    uploaded_songs: list[str]


@dataclass
class ArtistDTO(UserDTO):
    """Represents artist data in the endpoints transfer layer"""

    uploaded_songs: list[str]


def get_artist_dao_from_document(document: dict[str, Any]) -> ArtistDAO:
    """Get ArtistDAO from document

    Args:
    ----
        document (dict): user document

    Returns:
    -------
        ArtistDAO: ArtistDAO Object

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
        artist_dao (ArtistDAO): ArtistDAO object

    Returns:
    -------
        ArtistDTO: ArtistDTO object

    """
    return ArtistDTO(
        name=artist_dao.name,
        photo=artist_dao.photo,
        playback_history=artist_dao.playback_history,
        playlists=artist_dao.playlists,
        register_date=artist_dao.register_date,
        saved_playlists=artist_dao.saved_playlists,
        uploaded_songs=artist_dao.uploaded_songs,
    )
