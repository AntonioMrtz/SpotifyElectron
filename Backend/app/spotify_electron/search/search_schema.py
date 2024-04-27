from dataclasses import dataclass

from app.exceptions.exceptions_schema import SpotifyElectronException
from app.model.Artist import Artist
from app.model.DTO.SongDTO import SongDTO
from app.model.User import User
from app.spotify_electron.playlist.playlists_schema import PlaylistDTO


class SearchServiceException(SpotifyElectronException):
    """Exception for unexpected error in search service"""

    ERROR = "Unexpected error in search service"

    def __init__(self):
        super().__init__(self.ERROR)


@dataclass
class SearchResult:
    # TODO cambiar a DTOS cuando se implementen
    artists: list[Artist]
    playlists: list[PlaylistDTO]
    users: list[User]
    songs: list[SongDTO]
