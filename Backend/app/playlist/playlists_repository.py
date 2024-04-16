from sys import modules

from pymongo.results import DeleteResult, InsertOneResult

from app.database.Database import Database
from app.logging.logger_constants import LOGGING_PLAYLISTS_REPOSITORY
from app.logging.logging_schema import SpotifyElectronLogger
from app.playlist.playlists_schema import (
    PlaylistDAO,
    PlaylistDeleteException,
    PlaylistInsertException,
    PlaylistNotFoundException,
    PlaylistRepositoryException,
    get_playlist_dao_from_document,
)

if "pytest" in modules:
    playlist_collection = Database().connection["test.playlist"]

else:
    playlist_collection = Database().connection["playlist"]


playlist_repository_logger = SpotifyElectronLogger(
    LOGGING_PLAYLISTS_REPOSITORY
).getLogger()


def check_playlist_exists(name: str) -> bool:
    """Checks if playlist exists

    Args:
        name (str): name of the playlist

    Raises:
        PlaylistRepositoryException: an error ocurred while getting playlist from database

    Returns:
        bool: if the playlist exsists
    """
    try:
        playlist = playlist_collection.find_one({"name": name}, {"_id": 1})
    except Exception as exception:
        playlist_repository_logger.warning(
            f"Error checking if Playlist {name} exists in database"
        )
        raise PlaylistRepositoryException from exception
    else:
        return playlist is not None


def get_playlist_by_name(name: str) -> PlaylistDAO:
    """Get a playlist by name

    Args:
        name (str): name of the playlist

    Raises:
        PlaylistNotFoundException: playlists doesnt exists on database
        PlaylistRepositoryException: an error ocurred while getting playlist from database

    Returns:
        PlaylistDAO: the playlist with the name parameter
    """
    try:
        playlist = playlist_collection.find_one({"name": name})
        handle_playlist_exists(playlist)
        return get_playlist_dao_from_document(playlist)  # type: ignore

    except PlaylistNotFoundException as exception:
        raise PlaylistNotFoundException from exception

    except Exception as exception:
        playlist_repository_logger.exception(
            f"Error getting Playlist {name} from database"
        )
        raise PlaylistRepositoryException from exception


def insert_playlist(
    name: str,
    photo: str,
    upload_date: str,
    description: str,
    owner: str,
    song_names: list[str],
) -> None:
    """Inserts a Playlist

    Args:
        name (str): name
        photo (str): thumbnail photo
        upload_date (str): upload date
        description (str): description
        owner (str): playlist's owner
        song_names (list[str]): song names

    Raises:
        PlaylistRepositoryException: an error ocurred while inserting playlist in database

    """
    try:
        playlist = {
            "name": name,
            "photo": photo,
            "upload_date": upload_date,
            "description": description,
            "owner": owner,
            "song_names": song_names,
        }
        result = playlist_collection.insert_one(playlist)
        handle_playlist_insert(result)
    except PlaylistInsertException as exception:
        playlist_repository_logger.exception(
            f"Error inserting Playlist {name} in database"
        )
        raise PlaylistRepositoryException from exception
    except PlaylistRepositoryException as exception:
        playlist_repository_logger.exception(
            f"Unexpected error inserting playlist {name} in database"
        )
        raise PlaylistRepositoryException from exception
    else:
        playlist_repository_logger.debug(f"Playlist added to repository : {playlist}")


def delete_playlist(name: str) -> None:
    """Deletes a playlist

    Args:
        name (str): plalists name

    Raises:
        PlaylistRepositoryException: an error ocurred while deleting playlist from database
    """
    try:
        result = playlist_collection.delete_one({"name": name})
        handle_playlist_delete_count(result)
    except PlaylistDeleteException as exception:
        playlist_repository_logger.exception(
            f"Error deleting Playlist {name} from database"
        )
        raise PlaylistRepositoryException from exception
    except PlaylistRepositoryException as exception:
        playlist_repository_logger.exception(
            f"Unexpected error deleting playlist {name} in database"
        )
        raise PlaylistRepositoryException from exception


def get_all_playlists() -> list[PlaylistDAO]:
    """Get all playlist

    Raises:
        PlaylistRepositoryException: an error ocurred while getting all playlists from database

    Returns:
        list[PlaylistDAO]: the list whith all the playlists
    """
    try:
        playlists_files = playlist_collection.find()
        return [
            get_playlist_dao_from_document(playlist_file)
            for playlist_file in playlists_files
        ]
    except Exception as exception:
        playlist_repository_logger.exception(
            "Error getting all Playlists from database"
        )
        raise PlaylistRepositoryException from exception


def get_selected_playlists(names: list[str]) -> list[PlaylistDAO]:
    """Get selected playlists

    Args:
        names (list[str]): list with the names of the playlists

    Raises:
        PlaylistRepositoryException: an error ocurred while getting playlists from database

    Returns:
        list[PlaylistDAO]: the list of playlists
    """
    try:
        query = {"name": {"$in": names}}
        documents = playlist_collection.find(query)
        return [get_playlist_dao_from_document(document) for document in documents]
    except Exception as exception:
        playlist_repository_logger.exception(
            f"Error getting {names} Playlists from database"
        )
        raise PlaylistRepositoryException from exception


def get_playlist_search_by_name(name: str) -> list[PlaylistDAO]:
    """Gets the playlist with similar name

    Args:
        name (str): the matching name

    Raises:
        PlaylistRepositoryException: an error ocurred while getting playlist from database with simimilar name

    Returns:
        list[PlaylistDAO]: the list of playlists with similar name
    """
    try:
        documents = playlist_collection.find(
            {"name": {"$regex": name, "$options": "i"}}
        )
        return [get_playlist_dao_from_document(document) for document in documents]
    except Exception as exception:
        playlist_repository_logger.exception(
            f"Error getting Playlists searched by name {name} from database"
        )
        raise PlaylistRepositoryException from exception


def update_playlist(
    name: str,
    new_name: str,
    photo: str,
    description: str,
    song_names: list[str],
):
    # TODO
    try:
        playlist_collection.update_one(
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

    except Exception as exception:
        playlist_repository_logger.exception(f"Error updating playlist {name}")
        raise PlaylistRepositoryException from exception


def handle_playlist_exists(playlist: PlaylistDAO | None):
    """Raises an exception if playlist doesnt exists

    Args:
        playlist (PlaylistDAO | None): the playlist

    Raises:
        PlaylistNotFoundException: if the playlists doesnt exists
    """
    if playlist is None:
        raise PlaylistNotFoundException
    return


def handle_playlist_delete_count(result: DeleteResult):
    """Raises an exception if playlist deletion count was 0

    Args:
        result (DeleteResult): the result from the deletion

    Raises:
        PlaylistDeleteException: if the deletion was not done
    """
    if result.deleted_count == 0:
        raise PlaylistDeleteException
    return


def handle_playlist_insert(result: InsertOneResult):
    """Raises an exception if playlist insertion was not done

    Args:
        result (InsertOneResult): the result from the insertior

    Raises:
        PlaylistInsertException: if the insetion was not done
    """
    if result.acknowledged == 0:
        raise PlaylistInsertException
    return
