import app.services.artist_service as artist_service
import app.services.user_service as user_service
import app.spotify_electron.playlist.playlists_service as playlists_service
from app.exceptions.exceptions_schema import BadParameterException
from app.logging.logging_constants import LOGGING_SEARCH_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.services.song_services.song_service_provider import get_song_service
from app.services.utils import checkValidParameterString
from app.spotify_electron.search.search_schema import (
    SearchResult,
    SearchServiceException,
)

search_service_logger = SpotifyElectronLogger(LOGGING_SEARCH_SERVICE).getLogger()


song_service = get_song_service()


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
        checkValidParameterString(name)

        # TODO ASYNC
        songs = song_service.search_by_name(name)
        playlists = playlists_service.search_by_name(name)
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
