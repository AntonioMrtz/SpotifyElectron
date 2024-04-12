from datetime import datetime
from sys import modules

import app.repositories.playlist_repository as playlist_repository
import app.services.all_users_service as all_users_service
from app.constants.domain_constants import PLAYLIST
from app.database.Database import Database
from app.exceptions.repository_exceptions import (
    ItemNotFoundException,
    RepositoryException,
)
from app.exceptions.services_exceptions import (
    BadParameterException,
    ServiceException,
    UnAuthorizedException,
)
from app.logging.logger_constants import LOGGING_PLAYLISTS_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.model.Playlist import Playlist
from app.model.TokenData import TokenData
from app.services.song_services.song_service_provider import get_song_service
from app.services.utils import checkValidParameterString

if "pytest" in modules:
    playlist_collection = Database().connection["test.playlist"]

else:
    playlist_collection = Database().connection["playlist"]

song_service = get_song_service()

playlist_service_logger = SpotifyElectronLogger(LOGGING_PLAYLISTS_SERVICE).getLogger()


def check_jwt_user_is_playlist_owner(token: TokenData, owner: str) -> bool:
    """Check if the user is the playlist owner

    Parameters
    ----------
        token (TokenData): token with the user data
        owner (str) : owner of the playlist

    Raises
    -------
        Unauthorized 401

    Returns
    -------
        Boolean
    """

    if token.username == owner:
        return True
    raise UnAuthorizedException(owner)


def check_playlist_exists(name: str) -> bool:
    """Check if the song exists or not

    Parameters
    ----------
        name (str): Playlist's name

    Raises
    -------

    Returns
    -------
        Boolean
    """
    return playlist_repository.check_playlist_exists(name)


def get_playlist(name: str) -> Playlist:
    """Returns a Playlist with his songs

    Parameters
    ----------
        name (str): Playlists's name

    Raises
    -------
        400 : Bad Request
        404 : Playlist not found

    Returns
    -------
        Playlist object
    """
    try:
        playlist = playlist_repository.get_playlist_by_name(name)
        return playlist
    except BadParameterException:
        playlist_service_logger.error(f"Bad Parameter : {name}")
        raise
    except ItemNotFoundException:
        playlist_service_logger.error(f"Playlist not found : {name}")
        raise
    except RepositoryException as error:
        playlist_service_logger.error(
            f"Unhandled error in Playlist Repository : {error}"
        )
        raise ServiceException(PLAYLIST)
    except Exception as error:
        playlist_service_logger.error(f"Unhandled error in Playlist Service : {error}")
        raise ServiceException(PLAYLIST)


def create_playlist(
    name: str, photo: str, description: str, song_names: list, token: TokenData
) -> None:
    """Create a playlist with name, url of thumbnail and list of song names

    Parameters
    ----------
        name (str): Playlists's name
        photo (str): Url of playlist thumbnail
        description (str): Playlists's description
        song_names (list<str>): List of song names of the playlist
        token (TokenData) : token with user data

    Raises
    -------
        400 : Bad Request

    Returns
    -------
    """
    try:
        owner = token.username

        current_date = datetime.now()
        date_iso8601 = current_date.strftime("%Y-%m-%dT%H:%M:%S")

        checkValidParameterString(name)

        result_playlist_exists = playlist_repository.check_playlist_exists(name)
        if result_playlist_exists:
            raise BadParameterException(name)

        if not all_users_service.check_user_exists(owner):
            raise ItemNotFoundException(owner)

        playlist_repository.insert_playlist(
            name,
            photo if "http" in photo else "",
            date_iso8601,
            description,
            owner,
            song_names,
        )

        all_users_service.add_playlist_to_owner(
            user_name=owner, playlist_name=name, token=token
        )
    except BadParameterException:
        playlist_service_logger.error(f"Bad Parameter : {name}")
        raise
    except ItemNotFoundException:
        playlist_service_logger.error(f"Playlist not found : {name}")
        raise
    except RepositoryException as error:
        playlist_service_logger.error(
            f"Unhandled error in Playlist Repository : {error}"
        )
        raise ServiceException(PLAYLIST)
    except Exception as error:
        playlist_service_logger.error(f"Unhandled error in Playlist Service : {error}")
        raise ServiceException(PLAYLIST)


def update_playlist(
    name: str,
    new_name: str | None,
    photo: str,
    description: str,
    song_names: list,
    token: TokenData,
) -> None:
    """Updates a playlist with name, url of thumbnail and list of song names

    Parameters
    ----------
        name (str): Playlists's name
        nuevo_nombre (str) : New Playlist's name, if empty name is not being updated
        photo (str): Url of playlist thumbnail
        description (str): Playlists's description
        song_names (list<str>): List of song names of the playlist
        token (TokenData) : token with user data


    Raises
    -------
        400 : Bad Request
        404 : Playlist Not Found

    Returns
    -------
    """

    try:
        checkValidParameterString(name)

        result_playlist_exists = playlist_repository.check_playlist_exists(name)
        if not result_playlist_exists:
            raise ItemNotFoundException(name)

        playlist = playlist_repository.get_playlist_by_name(name)

        check_jwt_user_is_playlist_owner(token=token, owner=playlist.owner)

        if new_name is not None and checkValidParameterString(new_name):
            playlist_repository.update_playlist(
                name,
                new_name,
                photo if "http" in photo else "",
                description,
                song_names,
            )
            return
        playlist_repository.update_playlist(
            name, name, photo if "http" in photo else "", description, song_names
        )
    except BadParameterException:
        playlist_service_logger.error(f"Bad Parameter : {name}")
        raise
    except ItemNotFoundException:
        playlist_service_logger.error(f"Playlist not found : {name}")
        raise
    except RepositoryException as error:
        playlist_service_logger.error(
            f"Unhandled error in Playlist Repository : {error}"
        )
        raise ServiceException(PLAYLIST)
    except Exception as error:
        playlist_service_logger.error(f"Unhandled error in Playlist Service : {error}")
        raise ServiceException(PLAYLIST)


def delete_playlist(name: str) -> None:
    """Deletes a playlist by name

    Parameters
    ----------
        name (str): Playlists's name

    Raises
    -------
        400 : Bad Request
        404 : Playlist Not Found

    Returns
    -------
    """

    try:
        checkValidParameterString(name)
        all_users_service.delete_playlist_from_owner(playlist_name=name)
        playlist_repository.delete_playlist(name)
    except BadParameterException:
        playlist_service_logger.error(f"Bad Parameter : {name}")
        raise
    except ItemNotFoundException:
        playlist_service_logger.error(f"Playlist not found : {name}")
        raise
    except RepositoryException as error:
        playlist_service_logger.error(
            f"Unhandled error in Playlist Repository : {error}"
        )
        raise ServiceException(PLAYLIST)
    except Exception as error:
        playlist_service_logger.error(f"Unhandled error in Playlist Service : {error}")
        raise ServiceException(PLAYLIST)


def get_all_playlist() -> list[Playlist]:
    """Returns all playlists"

    Parameters
    ----------

    Raises
    -------
        400 : Bad Request
        404 : Playlist Not Found

    Returns
    -------
        List<Playlist>
    """

    try:
        playlists = playlist_repository.get_all_playlists()
        return playlists
    except RepositoryException as error:
        playlist_service_logger.error(
            f"Unhandled error in Playlist Repository : {error}"
        )
        raise ServiceException(PLAYLIST)
    except Exception as error:
        playlist_service_logger.error(f"Unhandled error in Playlist Service : {error}")
        raise ServiceException(PLAYLIST)


def get_selected_playlists(playlist_names: list[str]) -> list[Playlist]:
    """Returns the selected playlists"

    Parameters
    ----------
    playlist_names (list<str>) : the names of the playlists

    Raises
    -------
    400

    Returns
    -------
        List<Playlist>
    """

    try:
        playlists = playlist_repository.get_selected_playlists(playlist_names)
        return playlists
    except RepositoryException as error:
        playlist_service_logger.error(
            f"Unhandled error in Playlist Repository : {error}"
        )
        raise ServiceException(PLAYLIST)
    except Exception as error:
        playlist_service_logger.error(f"Unhandled error in Playlist Service : {error}")
        raise ServiceException(PLAYLIST)


def search_by_name(name: str) -> list[Playlist]:
    """Retrieve the playlists than match the name

    Args:
        name (str): the name to match

    Returns:
        List[Playlist]: a list with the playlists that match the name
    """
    try:
        playlists = playlist_repository.get_playlist_search_by_name(name)
        return playlists
    except RepositoryException as error:
        playlist_service_logger.error(
            f"Unhandled error in Playlist Repository : {error}"
        )
        raise ServiceException(PLAYLIST)
    except Exception as error:
        playlist_service_logger.error(f"Unhandled error in Playlist Service : {error}")
        raise ServiceException(PLAYLIST)
