"""
Search service for handling business logic
"""

from asyncio import create_task, gather

import app.spotify_electron.playlist.playlist_service as playlist_service
import app.spotify_electron.song.base_song_service as base_song_service
import app.spotify_electron.user.artist.artist_service as artist_service
import app.spotify_electron.user.user.user_service as user_service
from app.exceptions.base_exceptions_schema import BadParameterError
from app.logging.logging_constants import LOGGING_SEARCH_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.search.search_schema import (
    BadSearchParameterError,
    SearchResult,
    SearchServiceError,
)
from app.spotify_electron.utils.validations.validation_utils import validate_parameter

search_service_logger = SpotifyElectronLogger(LOGGING_SEARCH_SERVICE).get_logger()


async def search_by_name(name: str) -> SearchResult:
    """Return items that partially match the given name

    Args:
        name (str): the name to match

    Raises:
        BadSearchParameterError: invalid name for searching
        SearchServiceError: unexpected error getting items by name

    Returns:
        SearchResult: the items that partially match the name
    """
    try:
        validate_parameter(name)

        songs_task = create_task(base_song_service.search_by_name(name=name))
        playlists_task = create_task(playlist_service.search_by_name(name=name))
        artists_task = create_task(artist_service.search_by_name(name=name))
        users_task = create_task(user_service.search_by_name(name=name))

        songs, playlists, artists, users = await gather(
            *[
                songs_task,
                playlists_task,
                artists_task,
                users_task,
            ]
        )

    except BadParameterError as exception:
        search_service_logger.exception(f"Bad Search parameter: {name}")
        raise BadSearchParameterError from exception
    except Exception as exception:
        search_service_logger.exception(
            f"Unexpected error in Search Service searching for items with name: {name}"
        )
        raise SearchServiceError from exception
    else:
        search_results = SearchResult(artists, playlists, users, songs)
        search_service_logger.info(
            f"Items searched by name {name} retrieved successfully: {search_results}"
        )
        return search_results
