"""
Search schema for domain model
"""

from dataclasses import dataclass

from app.exceptions.base_exceptions_schema import SpotifyElectronException
from app.spotify_electron.playlist.playlist_schema import PlaylistDTO
from app.spotify_electron.song.base_song_schema import SongMetadataDTO
from app.spotify_electron.user.artist.artist_schema import ArtistDTO
from app.spotify_electron.user.user.user_schema import UserDTO


@dataclass
class SearchResult:
    """Class that contains the outcome of search operation"""

    artists: list[ArtistDTO]
    playlists: list[PlaylistDTO]
    users: list[UserDTO]
    songs: list[SongMetadataDTO]


class BadSearchParameterException(SpotifyElectronException):
    """Bad parameter provided for search"""

    ERROR = "Bad parameter provided for search"

    def __init__(self):
        super().__init__(self.ERROR)


class SearchServiceException(SpotifyElectronException):
    """Unexpected error in service"""

    ERROR = "Unexpected error in search service"

    def __init__(self):
        super().__init__(self.ERROR)
