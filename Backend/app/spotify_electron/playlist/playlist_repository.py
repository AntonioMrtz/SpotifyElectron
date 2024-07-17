"""
Playlist repository for managing persisted data
"""

from app.logging.logging_constants import LOGGING_PLAYLIST_REPOSITORY
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.playlist.playlist_schema import (
    PlaylistCreateException,
    PlaylistDAO,
    PlaylistDeleteException,
    PlaylistNotFoundException,
    PlaylistRepositoryException,
    get_playlist_dao_from_document,
)
from app.spotify_electron.playlist.providers.playlist_collection_provider import (
    get_playlist_collection,
)
from app.spotify_electron.playlist.validations.playlist_repository_validations import (
    validate_playlist_create,
    validate_playlist_delete_count,
    validate_playlist_exists,
    validate_playlist_update,
)

playlist_repository_logger = SpotifyElectronLogger(LOGGING_PLAYLIST_REPOSITORY).getLogger()


def check_playlist_exists(
    name: str,
) -> bool:
    """Checks if playlist exists

    Args:
    ----
        name (str): name of the playlist

    Raises:
    ------
        PlaylistRepositoryException: an error occurred while getting playlist from database

    Returns:
    -------
        bool: if the playlist exsists

    """
    try:
        collection = get_playlist_collection()
        playlist = collection.find_one({"name": name}, {"_id": 1})
    except Exception as exception:
        playlist_repository_logger.exception(
            f"Error checking if Playlist {name} exists in database"
        )
        raise PlaylistRepositoryException from exception
    else:
        result = playlist is not None
        playlist_repository_logger.debug(f"Playlist with name {name} exists : {result}")
        return result


def get_playlist(
    name: str,
) -> PlaylistDAO:
    """Get a playlist by name

    Args:
    ----
        name (str): name of the playlist


    Raises:
    ------
        PlaylistNotFoundException: playlists doesnt exists on database
        PlaylistRepositoryException: an error occurred while getting playlist from database

    Returns:
    -------
        PlaylistDAO: the playlist with the name parameter

    """
    try:
        collection = get_playlist_collection()
        playlist = collection.find_one({"name": name})
        validate_playlist_exists(playlist)
        playlist_dao = get_playlist_dao_from_document(playlist)  # type: ignore

    except PlaylistNotFoundException as exception:
        raise PlaylistNotFoundException from exception

    except Exception as exception:
        playlist_repository_logger.exception(f"Error getting Playlist {name} from database")
        raise PlaylistRepositoryException from exception
    else:
        playlist_repository_logger.info(f"Get Playlist by name returned {playlist_dao}")
        return playlist_dao


def create_playlist(  # noqa: PLR0913
    name: str,
    photo: str,
    upload_date: str,
    description: str,
    owner: str,
    song_names: list[str],
) -> None:
    """Creates a playlist

    Args:
    ----
        name (str): name
        photo (str): thumbnail photo
        upload_date (str): upload date
        description (str): description
        owner (str): playlist's owner
        song_names (list[str]): song names


    Raises:
    ------
        PlaylistRepositoryException: an error occurred while inserting playlist in database

    """
    try:
        collection = get_playlist_collection()
        playlist = {
            "name": name,
            "photo": photo,
            "upload_date": upload_date,
            "description": description,
            "owner": owner,
            "song_names": song_names,
        }
        result = collection.insert_one(playlist)
        validate_playlist_create(result)
    except PlaylistCreateException as exception:
        playlist_repository_logger.exception(
            f"Error inserting Playlist {playlist} in database"
        )
        raise PlaylistRepositoryException from exception
    except PlaylistRepositoryException as exception:
        playlist_repository_logger.exception(
            f"Unexpected error inserting playlist {playlist} in database"
        )
        raise PlaylistRepositoryException from exception
    else:
        playlist_repository_logger.info(f"Playlist added to repository : {playlist}")


def delete_playlist(
    name: str,
) -> None:
    """Deletes a playlist

    Args:
    ----
        name (str): plalists name


    Raises:
    ------
        PlaylistRepositoryException: an error occurred while deleting playlist from database

    """
    try:
        collection = get_playlist_collection()
        result = collection.delete_one({"name": name})
        validate_playlist_delete_count(result)
        playlist_repository_logger.info(f"Playlist {name} Deleted")
    except PlaylistDeleteException as exception:
        playlist_repository_logger.exception(f"Error deleting Playlist {name} from database")
        raise PlaylistRepositoryException from exception
    except PlaylistRepositoryException as exception:
        playlist_repository_logger.exception(
            f"Unexpected error deleting playlist {name} in database"
        )
        raise PlaylistRepositoryException from exception


def get_all_playlists() -> list[PlaylistDAO]:
    """Get all playlist


    Raises
    ------
        PlaylistRepositoryException: an error occurred while\
              getting all playlists from database

    Returns
    -------
        list[PlaylistDAO]: the list whith all the playlists

    """
    try:
        collection = get_playlist_collection()
        playlists_files = collection.find()
        playlists = [
            get_playlist_dao_from_document(playlist_file) for playlist_file in playlists_files
        ]
    except Exception as exception:
        playlist_repository_logger.exception("Error getting all Playlists from database")
        raise PlaylistRepositoryException from exception
    else:
        playlist_repository_logger.info(f"All playlists obtained : {playlists}")
        return playlists


def get_selected_playlists(
    names: list[str],
) -> list[PlaylistDAO]:
    """Get selected playlists

    Args:
    ----
        names (list[str]): list with the names of the playlists


    Raises:
    ------
        PlaylistRepositoryException: an error occurred while getting playlists from database

    Returns:
    -------
        list[PlaylistDAO]: the list of playlists

    """
    try:
        collection = get_playlist_collection()
        query = {"name": {"$in": names}}
        documents = collection.find(query)
        playlists = [get_playlist_dao_from_document(document) for document in documents]
    except Exception as exception:
        playlist_repository_logger.exception(f"Error getting {names} Playlists from database")
        raise PlaylistRepositoryException from exception
    else:
        playlist_repository_logger.info(
            f"Selected playlists obtained for {names} : {playlists}"
        )
        return playlists


def get_playlist_search_by_name(
    name: str,
) -> list[PlaylistDAO]:
    """Gets the playlist with similar name

    Args:
    ----
        name (str): the matching name


    Raises:
    ------
        PlaylistRepositoryException: an error occurred while getting playlist from database\
              with simimilar name

    Returns:
    -------
        list[PlaylistDAO]: the list of playlists with similar name

    """
    try:
        collection = get_playlist_collection()
        documents = collection.find({"name": {"$regex": name, "$options": "i"}})
        playlists = [get_playlist_dao_from_document(document) for document in documents]
    except Exception as exception:
        playlist_repository_logger.exception(
            f"Error getting Playlists searched by name {name} from database"
        )
        raise PlaylistRepositoryException from exception
    else:
        playlist_repository_logger.info(f"Playlist searched by name {name} : {playlists}")
        return playlists


def update_playlist(
    name: str,
    new_name: str,
    photo: str,
    description: str,
    song_names: list[str],
):
    """Update playlist

    Args:
        name (str): playlist name
        new_name (str): new name
        photo (str): new photo
        description (str): new description
        song_names (list[str]): new song names

    Raises:
        PlaylistRepositoryException: unexpected error updating playlist
    """
    try:
        collection = get_playlist_collection()
        result_update = collection.update_one(
            {"name": name},
            {
                "$set": {
                    "name": new_name,
                    "description": description,
                    "photo": photo,
                    "song_names": list(set(song_names)),
                }
            },
        )
        validate_playlist_update(result_update)

    except PlaylistCreateException as exception:
        playlist_repository_logger.exception(
            f"Error updating playlist {name}:\n"
            f"new_name = {new_name},\n"
            f"photo = {photo},\n"
            f"description = {description},\n"
            f"song_names = {song_names}"
        )
        raise PlaylistRepositoryException from exception

    except Exception as exception:
        playlist_repository_logger.exception(
            f"Unexpected error updating playlist {name}:\n"
            f"new_name = {new_name},\n"
            f"photo = {photo},\n"
            f"description = {description},\n"
            f"song_names = {song_names}"
        )
        raise PlaylistRepositoryException from exception

    else:
        playlist_repository_logger.info(
            f"Playlist {name} updated:\n"
            f"new_name = {new_name},\n"
            f"photo = {photo},\n"
            f"description = {description},\n"
            f"song_names = {song_names}"
        )
