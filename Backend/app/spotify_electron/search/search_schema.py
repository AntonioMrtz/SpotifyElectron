from dataclasses import dataclass

from app.exceptions.exceptions_schema import SpotifyElectronException
from app.model.DTO.SongDTO import SongDTO
from app.spotify_electron.playlist.playlist_schema import PlaylistDTO
from app.spotify_electron.user.artist.artist_schema import Artist
from app.spotify_electron.user.user_schema import User


@dataclass
class SearchResult:
    """A class that contains the outcome of search operation"""

    # TODO cambiar a DTOS cuando se implementen
    artists: list[Artist]
    playlists: list[PlaylistDTO]
    users: list[User]
    songs: list[SongDTO]


class BadSearchParameterException(SpotifyElectronException):
    """Exception for bad parameter provided for search"""

    ERROR = "Bad parameter provided for search"

    def __init__(self):
        super().__init__(self.ERROR)


class SearchServiceException(SpotifyElectronException):
    """Exception for unexpected error in search service"""

    ERROR = "Unexpected error in search service"

    def __init__(self):
        super().__init__(self.ERROR)
