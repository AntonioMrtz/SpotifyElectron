import app.services.song_services.song_service_provider as song_service_provider
import app.spotify_electron.playlist.playlist_service as playlist_service
import app.spotify_electron.user.artist.artist_service as artist_service
import app.spotify_electron.user.user_service as user_service
from app.exceptions.exceptions_schema import BadParameterException
from app.logging.logging_constants import LOGGING_SEARCH_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.search.search_schema import (
    SearchResult,
    SearchServiceException,
)
from app.spotify_electron.utils.validation.utils import validate_parameter

search_service_logger = SpotifyElectronLogger(LOGGING_SEARCH_SERVICE).getLogger()


def search_by_name(name: str) -> SearchResult:
    """Return items that partially match the given name

    Args:
        name (str): the name to match

    Raises:
        BadParameterException: if the name is invalid
        SearchServiceException: if unexpected error getting items by name

    Returns:
        SearchResult: the items that partially match the name
    """
    try:
        validate_parameter(name)

        # TODO ASYNC
        songs = song_service_provider.song_service.search_by_name(name)
        playlists = playlist_service.search_by_name(name)
        artists = artist_service.search_by_name(name)
        users = user_service.search_by_name(name)

    except BadParameterException as exception:
        search_service_logger.exception(f"Bad parameter : {name}")
        raise BadParameterException(name) from exception
    except Exception as exception:
        search_service_logger.exception(
            f"Unexpected error in Search Service searching for items with name : {name}"
        )
        raise SearchServiceException from exception
    else:
        search_results = SearchResult(artists, playlists, users, songs)
        search_service_logger.info(
            f"Items searched by name {name} retrieved successfully : {search_results}"
        )
        return search_results
