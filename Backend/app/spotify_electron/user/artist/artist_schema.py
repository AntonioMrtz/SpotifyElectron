"""
Artist schema for User domain model
"""

from dataclasses import dataclass
from typing import Any

from app.spotify_electron.song.base_song_repository import get_artist_total_streams
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
    """Creates an ArtistDAO object from a document dictionary.

    Args:
       document: Dictionary containing artist data.

    Returns:
       An ArtistDAO object populated with the document data.
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
        total_streams=get_artist_total_streams(document["name"]),
    )


def get_artist_dto_from_dao(artist_dao: ArtistDAO) -> ArtistDTO:
    """Converts an ArtistDAO object to an ArtistDTO object.

    Args:
       artist_dao: The ArtistDAO object to convert.

    Returns:
       An ArtistDTO object containing the artist data.
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
