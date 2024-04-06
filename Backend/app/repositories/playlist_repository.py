from sys import modules
from typing import List

from app.constants.domain_constants import PLAYLIST
from app.database.Database import Database
from app.exceptions.repository_exceptions import (
    ItemNotFoundException,
    RepositoryException,
)
from app.logging.logger_constants import LOGGING_PLAYLISTS_REPOSITORY
from app.logging.logging_schema import SpotifyElectronLogger
from app.model.Playlist import Playlist

if "pytest" in modules:
    playlist_collection = Database().connection["test.playlist"]

else:
    playlist_collection = Database().connection["playlist"]


playlist_repository_logger = SpotifyElectronLogger(
    LOGGING_PLAYLISTS_REPOSITORY
).getLogger()


def check_playlist_exists(name: str) -> bool:
    try:
        playlist = playlist_collection.find_one({"name": name}, {"_id": 1})
        return playlist is not None
    except Exception as error:
        playlist_repository_logger.error(
            f"Error checking if Playlist {name} exists in database : {error}"
        )
        raise RepositoryException(PLAYLIST)


def get_playlist_by_name(name: str) -> Playlist:
    try:
        playlist = playlist_collection.find_one({"name": name})
        if playlist is None:
            raise ItemNotFoundException(PLAYLIST)
        return get_playlist_from_document(playlist)

    except ItemNotFoundException:
        raise

    except Exception as error:
        playlist_repository_logger.error(
            f"Error getting Playlist {name} from database : {error}"
        )
        raise RepositoryException(PLAYLIST)


def insert_playlist(
    name: str,
    photo: str,
    upload_date: str,
    description: str,
    owner: str,
    song_names: List[str],
):
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
        if not result.acknowledged:
            raise Exception("Playlist was not added to the repository")
        playlist_repository_logger.debug(f"Playlist added to repository : {playlist}")
        return result
    except Exception as error:
        playlist_repository_logger.error(
            f"Error inserting Playlist {name} in database : {error}"
        )
        raise RepositoryException(PLAYLIST)


def delete_playlist(name: str):
    try:
        result = playlist_collection.delete_one({"name": name})
        if result.deleted_count == 0:
            raise ItemNotFoundException(name)
    except ItemNotFoundException:
        raise
    except Exception as error:
        playlist_repository_logger.error(
            f"Error deleting Playlist {name} from database : {error}"
        )
        raise RepositoryException(PLAYLIST)


def get_all_playlists() -> List[Playlist]:
    try:
        playlists_files = playlist_collection.find()
        return [
            get_playlist_from_document(playlist_file)
            for playlist_file in playlists_files
        ]
    except Exception as error:
        playlist_repository_logger.error(
            f"Error getting all Playlists from database : {error}"
        )
        raise RepositoryException(PLAYLIST)


def get_selected_playlists(names: List[str]) -> List[Playlist]:
    try:
        query = {"name": {"$in": names}}
        documents = playlist_collection.find(query)
        return [get_playlist_from_document(document) for document in documents]
    except Exception as error:
        playlist_repository_logger.error(
            f"Error getting {names} Playlists from database : {error}"
        )
        raise RepositoryException(PLAYLIST)


def get_playlist_search_by_name(name: str) -> List[Playlist]:
    try:
        documents = playlist_collection.find(
            {"name": {"$regex": name, "$options": "i"}}
        )
        return [get_playlist_from_document(document) for document in documents]
    except Exception as error:
        playlist_repository_logger.error(
            f"Error getting Playlists searched by name {name} from database : {error}"
        )
        raise RepositoryException(PLAYLIST)


def update_playlist(
    name: str,
    new_name: str,
    photo: str,
    description: str,
    song_names: List[str],
):
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

    except Exception as error:
        playlist_repository_logger.error(f"Error updating playlist {name} : {error}")
        raise RepositoryException(PLAYLIST)


def get_playlist_from_document(document: dict) -> Playlist:
    return Playlist(
        document["name"],
        document["photo"],
        document["description"],
        document["upload_date"][:-1],
        document["owner"],
        document["song_names"],
    )
