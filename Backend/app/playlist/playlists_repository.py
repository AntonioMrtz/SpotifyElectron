from sys import modules

from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from app.database.Database import Database
from app.logging.logger_constants import LOGGING_PLAYLIST_REPOSITORY
from app.logging.logging_schema import SpotifyElectronLogger
from app.playlist.playlists_schema import (
    PlaylistDAO,
    PlaylistDeleteException,
    PlaylistInsertException,
    PlaylistNotFoundException,
    PlaylistRepositoryException,
    PlaylistUpdateException,
    get_playlist_dao_from_document,
)

if "pytest" in modules:
    playlist_collection = Database.get_instance().connection["test.playlist"]

else:
    playlist_collection = Database.get_instance().connection["playlist"]


playlist_repository_logger = SpotifyElectronLogger(
    LOGGING_PLAYLIST_REPOSITORY
).getLogger()


def check_playlist_exists(name: str) -> bool:
    """Checks if playlist exists

    Args:
        name (str): name of the playlist

    Raises:
        PlaylistRepositoryException: an error occurred while getting playlist from database

    Returns:
        bool: if the playlist exsists
    """
    try:
        playlist = playlist_collection.find_one({"name": name}, {"_id": 1})
    except Exception as exception:
        playlist_repository_logger.critical(
            f"Error checking if Playlist {name} exists in database"
        )
        raise PlaylistRepositoryException from exception
    else:
        result = playlist is not None
        playlist_repository_logger.debug(f"Playlist with name {name} exists : {result}")
        return result


def get_playlist_by_name(name: str) -> PlaylistDAO:
    """Get a playlist by name

    Args:
        name (str): name of the playlist

    Raises:
        PlaylistNotFoundException: playlists doesnt exists on database
        PlaylistRepositoryException: an error occurred while getting playlist from database

    Returns:
        PlaylistDAO: the playlist with the name parameter
    """
    try:
        playlist = playlist_collection.find_one({"name": name})
        handle_playlist_exists(playlist)
        playlist_dao = get_playlist_dao_from_document(playlist)  # type: ignore

    except PlaylistNotFoundException as exception:
        raise PlaylistNotFoundException from exception

    except Exception as exception:
        playlist_repository_logger.critical(
            f"Error getting Playlist {name} from database"
        )
        raise PlaylistRepositoryException from exception
    else:
        playlist_repository_logger.debug(
            f"Get Playlist by name returned {playlist_dao}"
        )
        return playlist_dao


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
        PlaylistRepositoryException: an error occurred while inserting playlist in database

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
            f"Error inserting Playlist {playlist} in database"
        )
        raise PlaylistRepositoryException from exception
    except PlaylistRepositoryException as exception:
        playlist_repository_logger.critical(
            f"Unexpected error inserting playlist {playlist} in database"
        )
        raise PlaylistRepositoryException from exception
    else:
        playlist_repository_logger.info(f"Playlist added to repository : {playlist}")


def delete_playlist(name: str) -> None:
    """Deletes a playlist

    Args:
        name (str): plalists name

    Raises:
        PlaylistRepositoryException: an error occurred while deleting playlist from database
    """
    try:
        result = playlist_collection.delete_one({"name": name})
        handle_playlist_delete_count(result)
        playlist_repository_logger.debug(f"Playlist {name} Deleted")
    except PlaylistDeleteException as exception:
        playlist_repository_logger.exception(
            f"Error deleting Playlist {name} from database"
        )
        raise PlaylistRepositoryException from exception
    except PlaylistRepositoryException as exception:
        playlist_repository_logger.critical(
            f"Unexpected error deleting playlist {name} in database"
        )
        raise PlaylistRepositoryException from exception


def get_all_playlists() -> list[PlaylistDAO]:
    """Get all playlist

    Raises:
        PlaylistRepositoryException: an error occurred while getting all playlists from database

    Returns:
        list[PlaylistDAO]: the list whith all the playlists
    """
    try:
        playlists_files = playlist_collection.find()
        playlists = [
            get_playlist_dao_from_document(playlist_file)
            for playlist_file in playlists_files
        ]
    except Exception as exception:
        playlist_repository_logger.exception(
            "Error getting all Playlists from database"
        )
        raise PlaylistRepositoryException from exception
    else:
        playlist_repository_logger.debug(f"All playlists obtained : {playlists}")
        return playlists


def get_selected_playlists(names: list[str]) -> list[PlaylistDAO]:
    """Get selected playlists

    Args:
        names (list[str]): list with the names of the playlists

    Raises:
        PlaylistRepositoryException: an error occurred while getting playlists from database

    Returns:
        list[PlaylistDAO]: the list of playlists
    """
    try:
        query = {"name": {"$in": names}}
        documents = playlist_collection.find(query)
        playlists = [get_playlist_dao_from_document(document) for document in documents]
    except Exception as exception:
        playlist_repository_logger.critical(
            f"Error getting {names} Playlists from database"
        )
        raise PlaylistRepositoryException from exception
    else:
        playlist_repository_logger.debug(
            f"Selected playlists obtained for {names} : {playlists}"
        )
        return playlists


def get_playlist_search_by_name(name: str) -> list[PlaylistDAO]:
    """Gets the playlist with similar name

    Args:
        name (str): the matching name

    Raises:
        PlaylistRepositoryException: an error occurred while getting playlist from database with simimilar name

    Returns:
        list[PlaylistDAO]: the list of playlists with similar name
    """
    try:
        documents = playlist_collection.find(
            {"name": {"$regex": name, "$options": "i"}}
        )
        playlists = [get_playlist_dao_from_document(document) for document in documents]
    except Exception as exception:
        playlist_repository_logger.critical(
            f"Error getting Playlists searched by name {name} from database"
        )
        raise PlaylistRepositoryException from exception
    else:
        playlist_repository_logger.debug(
            f"Playlist searched by name {name} : {playlists}"
        )
        return playlists


def update_playlist(
    name: str,
    new_name: str,
    photo: str,
    description: str,
    song_names: list[str],
):
    """Updates playlist fields

    :param str name: current name
    :param str new_name: new name
    :param str photo: new photo
    :param str description: new description
    :param list[str] song_names: new list of song names
    :raises PlaylistRepositoryException: an error occurred while updating
    """
    try:
        result_update = playlist_collection.update_one(
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
        handle_playlist_update(result_update)

    except PlaylistInsertException as exception:
        playlist_repository_logger.critical(
            f"Error updating playlist {name} : new_name = {new_name}, photo = {photo}, description = {description}, song_names = {song_names}"
        )
        raise PlaylistRepositoryException from exception

    except Exception as exception:
        playlist_repository_logger.critical(
            f"Unexpected error updating playlist {name} : new_name = {new_name}, photo = {photo}, description = {description}, song_names = {song_names}"
        )
        raise PlaylistRepositoryException from exception
    else:
        playlist_repository_logger.critical(
            f"Playlisy {name} updated : new_name = {new_name}, photo = {photo}, description = {description}, song_names = {song_names}"
        )


def handle_playlist_exists(playlist: PlaylistDAO | None) -> None:
    """Raises an exception if playlist doesnt exists

    Args:
        playlist (PlaylistDAO | None): the playlist

    Raises:
        PlaylistNotFoundException: if the playlists doesnt exists
    """
    if playlist is None:
        raise PlaylistNotFoundException


def handle_playlist_delete_count(result: DeleteResult) -> None:
    """Raises an exception if playlist deletion count was 0

    Args:
        result (DeleteResult): the result from the deletion

    Raises:
        PlaylistDeleteException: if the deletion was not done
    """
    if result.deleted_count == 0:
        raise PlaylistDeleteException


def handle_playlist_update(result: UpdateResult) -> None:
    """Raises an exception if playlist deletion count was 0

    Args:
        result (DeleteResult): the result from the deletion

    Raises:
        PlaylistDeleteException: if the deletion was not done
    """
    if not result.acknowledged:
        raise PlaylistUpdateException


def handle_playlist_insert(result: InsertOneResult) -> None:
    """Raises an exception if playlist insertion was not done

    Args:
        result (InsertOneResult): the result from the insertior

    Raises:
        PlaylistInsertException: if the insetion was not done
    """
    if not result.acknowledged:
        raise PlaylistInsertException
