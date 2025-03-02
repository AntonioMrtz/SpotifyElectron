"""
Artist repository for managing persisted data
"""

import app.spotify_electron.user.providers.user_collection_provider as user_collection_provider
from app.logging.logging_constants import LOGGING_ARTIST_REPOSITORY
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.user.artist.artist_schema import (
    ArtistDAO,
    ArtistNotFoundError,
    ArtistRepositoryError,
    get_artist_dao_from_document,
)
from app.spotify_electron.user.base_user_schema import (
    BaseUserCreateError,
    BaseUserNotFoundError,
    BaseUserUpdateError,
)
from app.spotify_electron.user.user.user_schema import UserDAO
from app.spotify_electron.user.validations.base_user_repository_validations import (
    validate_user_create,
    validate_user_exists,
    validate_user_update,
)

artist_repository_logger = SpotifyElectronLogger(LOGGING_ARTIST_REPOSITORY).get_logger()


def get_artist(name: str) -> ArtistDAO:
    """Get artist by name

    Args:
        name (str): artist name

    Raises:
        ArtistNotFoundError: artist was not found
        ArtistRepositoryError: unexpected error while getting artist

    Returns:
        ArtistDAO: the artist
    """
    try:
        artist = user_collection_provider.get_artist_collection().find_one({"name": name})
        validate_user_exists(artist)
        artist_dao = get_artist_dao_from_document(artist)  # type: ignore

    except BaseUserNotFoundError as exception:
        raise ArtistNotFoundError from exception

    except Exception as exception:
        artist_repository_logger.exception(f"Error getting User {name} from database")
        raise ArtistRepositoryError from exception
    else:
        artist_repository_logger.info(f"Get Artist by name returned {artist_dao}")
        return artist_dao


def create_artist(name: str, photo: str, password: bytes, current_date: str) -> None:
    """Create artist

    Args:
        name (str): artist name
        photo (str): artist photo
        password (bytes): artist hashed password
        current_date (str): formatted creation date

    Raises:
        ArtistRepositoryError: unexpected error while creating Artist
    """
    try:
        artist = {
            "name": name,
            "photo": photo,
            "register_date": current_date,
            "password": password,
            "saved_playlists": [],
            "playlists": [],
            "playback_history": [],
            "uploaded_songs": [],
        }
        result = user_collection_provider.get_artist_collection().insert_one(artist)

        validate_user_create(result)
    except BaseUserCreateError as exception:
        artist_repository_logger.exception(f"Error inserting Artist {artist} in database")
        raise ArtistRepositoryError from exception
    except (ArtistRepositoryError, Exception) as exception:
        artist_repository_logger.exception(
            f"Unexpected error inserting artist {artist} in database"
        )
        raise ArtistRepositoryError from exception
    else:
        artist_repository_logger.info(f"Artist added to repository: {artist}")


def create_artist_from_user_dao(user: UserDAO) -> None:
    """Create artist from existing user data

    Args:
        user (UserDAO): Existing user data

    Raises:
        ArtistRepositoryError: Unexpected error while creating artist
    """
    try:
        artist = {
            "name": user.name,
            "photo": user.photo,
            "current_date": user.register_date,
            "password": user.password,
        }
        create_artist(**artist)
        missing_fields = {
            "saved_playlists": user.saved_playlists if user.saved_playlists else [],
            "playlists": user.playlists if user.saved_playlists else [],
            "playback_history": user.playback_history if user.saved_playlists else [],
            "uploaded_songs": [],
        }
        result = user_collection_provider.get_artist_collection().update_one(
            {"name": user.name}, {"$set": missing_fields}
        )
        validate_user_update(result)

    except BaseUserCreateError as exception:
        artist_repository_logger.exception(
            f"Error inserting Artist from user {user.name} in database"
        )
        raise ArtistRepositoryError from exception
    except BaseUserUpdateError as exception:
        artist_repository_logger.exception(
            f"Error updating missing field into Artist {user.name}"
        )
        raise ArtistRepositoryError from exception
    except Exception as exception:
        artist_repository_logger.exception(
            f"Unexpected error creating artist from user {user.name}"
        )
        raise ArtistRepositoryError from exception
    else:
        artist_repository_logger.info(f"Artist created from user: {user.name}")


def get_all_artists() -> list[ArtistDAO]:
    """Get all artists

    Raises:
        ArtistRepositoryError: unexpected error getting all artists

    Returns:
        list[ArtistDAO]: a list with all artists
    """
    try:
        artists = [
            get_artist_dao_from_document(artist)
            for artist in user_collection_provider.get_artist_collection().find()
        ]
    except Exception as exception:
        artist_repository_logger.exception("Error getting all artists names from database")
        raise ArtistRepositoryError from exception
    else:
        artist_repository_logger.info("All artists names retrieved successfully")
        return artists


def add_song_to_artist(artist_name: str, song_name: str) -> None:
    """Add song to artist

    Args:
        artist_name (str): artist name
        song_name (str): song name

    Raises:
        ArtistRepositoryError: unexpected error adding song to artist
    """
    try:
        result = user_collection_provider.get_artist_collection().update_one(
            {"name": artist_name}, {"$push": {"uploaded_songs": song_name}}
        )
        validate_user_update(result)
    except BaseUserUpdateError as exception:
        artist_repository_logger.exception(
            f"Error updating artist {artist_name} with song {song_name} in database"
        )
        raise ArtistRepositoryError from exception
    except (ArtistRepositoryError, Exception) as exception:
        artist_repository_logger.exception(
            f"Unexpected error adding song {song_name} to artist {artist_name} in database"
        )
        raise ArtistRepositoryError from exception


def delete_song_from_artist(artist_name: str, song_name: str) -> None:
    """Delete song from artist

    Args:
        artist_name (str): artist name
        song_name (str): song name

    Raises:
        ArtistRepositoryError: unexpected error deleting song from artist
    """
    try:
        result = user_collection_provider.get_artist_collection().update_one(
            {"name": artist_name}, {"$pull": {"uploaded_songs": song_name}}
        )
        validate_user_update(result)
    except BaseUserUpdateError as exception:
        artist_repository_logger.exception(
            f"Error updating artist {artist_name} with deletion of "
            f"song {song_name} in database"
        )
        raise ArtistRepositoryError from exception
    except (ArtistRepositoryError, Exception) as exception:
        artist_repository_logger.exception(
            f"Unexpected error removing song {song_name} from artist {artist_name} in database"
        )
        raise ArtistRepositoryError from exception


def get_artist_song_names(artist_name: str) -> list[str]:
    """Get artist song names

    Args:
        artist_name (str): artist name

    Returns:
        list[str]: the artist uploaded song names
    """
    artist_data = user_collection_provider.get_artist_collection().find_one(
        {"name": artist_name}, {"uploaded_songs": 1, "_id": 0}
    )

    return artist_data["uploaded_songs"]  # type: ignore
