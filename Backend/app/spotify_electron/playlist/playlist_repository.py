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
    PlaylistUpdateException,
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
    """Checks if a playlist exists in the database.

    Args:
       name: Name of the playlist to check.

    Returns:
       True if the playlist exists, False otherwise.

    Raises:
       PlaylistRepositoryException: If an error occurs while checking the database.
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
        playlist_repository_logger.debug(f"Playlist with name {name} exists: {result}")
        return result


def get_playlist(
    name: str,
) -> PlaylistDAO:
    """Retrieves a playlist by its name.

    Args:
       name: Name of the playlist to retrieve.

    Returns:
       A PlaylistDAO object containing the playlist data.

    Raises:
       PlaylistNotFoundException: If the playlist does not exist.
       PlaylistRepositoryException: If an error occurs while retrieving playlist.
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
    """Creates a new playlist in the database.

    Args:
       name: Name of the playlist.
       photo: URL of the playlist thumbnail.
       upload_date: Date when the playlist was created.
       description: Description of the playlist.
       owner: Username of the playlist owner.
       song_names: List of songs in the playlist.

    Raises:
       PlaylistRepositoryException: If an error occurs while creating the playlist.
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
        playlist_repository_logger.info(f"Playlist added to repository: {playlist}")


def delete_playlist(
    name: str,
) -> None:
    """Deletes a playlist from the database.

    Args:
       name: Name of the playlist to delete.

    Raises:
       PlaylistRepositoryException: If an error occurs while deleting the playlist.
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
    """Retrieves all playlists from the database.

    Returns:
       List of all PlaylistDAO objects in the database.

    Raises:
       PlaylistRepositoryException: If an error occurs while retrieving playlists.
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
        playlist_repository_logger.info(f"All playlists obtained: {playlists}")
        return playlists


def get_selected_playlists(
    names: list[str],
) -> list[PlaylistDAO]:
    """Retrieves multiple playlists by their names.

    Args:
       names: List of playlist names to retrieve.

    Returns:
       List of PlaylistDAO objects for the requested playlists.

    Raises:
       PlaylistRepositoryException: If an error occurs while retrieving playlists.
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
            f"Selected playlists obtained for {names}: {playlists}"
        )
        return playlists


def get_playlist_search_by_name(
    name: str,
) -> list[PlaylistDAO]:
    """Searches for playlists with names matching a pattern.

    Args:
       name: Search pattern to match against playlist names.

    Returns:
       List of PlaylistDAO objects with names matching the pattern.

    Raises:
       PlaylistRepositoryException: If an error occurs while searching the database.
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
        playlist_repository_logger.info(f"Playlist searched by name {name}: {playlists}")
        return playlists


def update_playlist(
    name: str,
    new_name: str,
    photo: str,
    description: str,
    song_names: list[str],
) -> None:
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

    except PlaylistUpdateException as exception:
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


def add_songs_to_playlist(name: str, song_names: list[str]) -> None:
    """Add songs to playlist

    Args:
        name (str): playlist name
        song_names (list[str]): song names

    Raises:
        PlaylistRepositoryException: unexpected error adding songs to playlist
    """
    try:
        collection = get_playlist_collection()
        result_update = collection.update_one(
            {"name": name}, {"$addToSet": {"song_names": {"$each": song_names}}}
        )
        validate_playlist_update(result_update)
    except PlaylistUpdateException as exception:
        playlist_repository_logger.info(f"Error adding songs to playlist {name}: {song_names}")
        raise PlaylistRepositoryException from exception
    except Exception as exception:
        playlist_repository_logger.info(
            f"Unexpected error adding songs to playlist {name}: {song_names}"
        )
        raise PlaylistRepositoryException from exception
    else:
        playlist_repository_logger.info(f"Songs added to playlist {name}: {song_names}")


def remove_songs_from_playlist(name: str, song_names: list[str]) -> None:
    """Remove songs from playlist

    Args:
        name (str): playlist name
        song_names (list[str]): song names

    Raises:
        PlaylistRepositoryException: unexpected error adding songs to playlist
    """
    try:
        collection = get_playlist_collection()
        result_update = collection.update_one(
            {"name": name},
            {"$pull": {"song_names": {"$in": song_names}}},
        )
        validate_playlist_update(result_update)
    except PlaylistUpdateException as exception:
        playlist_repository_logger.info(
            f"Error removing songs from playlist {name}: {song_names}"
        )
        raise PlaylistRepositoryException from exception
    except Exception as exception:
        playlist_repository_logger.info(
            f"Unexpected error removing songs from playlist {name}: {song_names}"
        )
        raise PlaylistRepositoryException from exception
    else:
        playlist_repository_logger.info(f"Songs removed from playlist {name}: {song_names}")
