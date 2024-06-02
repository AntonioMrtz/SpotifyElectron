import app.spotify_electron.user.providers.user_collection_provider as user_collection_provider
from app.logging.logging_constants import LOGGING_ARTIST_REPOSITORY
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.user.artist.artist_schema import (
    ArtistDAO,
    get_artist_dao_from_document,
)
from app.spotify_electron.user.user.user_schema import (
    UserCreateException,
    UserNotFoundException,
    UserRepositoryException,
)
from app.spotify_electron.user.validations.base_users_repository_validations import (
    validate_user_create,
    validate_user_exists,
    validate_user_update,
)

artist_repository_logger = SpotifyElectronLogger(LOGGING_ARTIST_REPOSITORY).getLogger()


def get_user(name: str) -> ArtistDAO:
    """Get user by name

    Args:
        name (str): user name

    Raises:
        UserNotFoundException: user was not found
        UserRepositoryException: unexpected error while getting user

    Returns:
        UserDAO: the user
    """
    try:
        artist = user_collection_provider.get_artist_collection().find_one(
            {"name": name}
        )
        validate_user_exists(artist)
        artist_dao = get_artist_dao_from_document(artist)  # type: ignore

    except UserNotFoundException as exception:
        raise UserNotFoundException from exception

    except Exception as exception:
        artist_repository_logger.exception(f"Error getting User {name} from database")
        raise UserRepositoryException from exception
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
        UserRepositoryException: unexpected error while creating user
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
    except UserCreateException as exception:
        artist_repository_logger.exception(
            f"Error inserting Artist {artist} in database"
        )
        raise UserRepositoryException from exception
    except (UserRepositoryException, Exception) as exception:
        artist_repository_logger.exception(
            f"Unexpected error inserting artist {artist} in database"
        )
        raise UserRepositoryException from exception
    else:
        artist_repository_logger.info(f"Artist added to repository : {artist}")


def get_all_artists() -> list[ArtistDAO]:
    """Get all artists

    Raises:
        UserRepositoryException: unexpected error getting all artists

    Returns:
        list[ArtistDAO]: a list with all artists
    """
    try:
        artists = [
            get_artist_dao_from_document(artist)
            for artist in user_collection_provider.get_artist_collection().find()
        ]
    except Exception as exception:
        artist_repository_logger.exception(
            "Error getting all artists names from database"
        )
        raise UserRepositoryException from exception
    else:
        artist_repository_logger.info("All artists names retrieved successfully")
        return artists


def add_song_to_artist(artist_name: str, song_name: str) -> None:
    """Add song to artist

    Args:
        artist_name (str): artist name
        song_name (str): song name

    Raises:
        UserRepositoryException: unexpected error adding song to artist
    """
    try:
        result = user_collection_provider.get_artist_collection().update_one(
            {"name": artist_name}, {"$push": {"uploaded_songs": song_name}}
        )
        validate_user_update(result)
    except UserCreateException as exception:
        artist_repository_logger.exception(
            f"Error updating artist {artist_name} with song {song_name} in database"
        )
        raise UserRepositoryException from exception
    except (UserRepositoryException, Exception) as exception:
        artist_repository_logger.exception(
            f"Unexpected error adding song {song_name} to artist {artist_name} in database"
        )
        raise UserRepositoryException from exception


def delete_song_from_artist(artist_name: str, song_name: str) -> None:
    """Delete song from artist

    Args:
        artist_name (str): artist name
        song_name (str): song name

    Raises:
        UserRepositoryException: unexpected error deleting song from artist
    """
    try:
        result = user_collection_provider.get_artist_collection().update_one(
            {"name": artist_name}, {"$pull": {"uploaded_songs": song_name}}
        )
        validate_user_update(result)
    except UserCreateException as exception:
        artist_repository_logger.exception(
            f"Error updating artist {artist_name} with deletion of song {song_name} in database"
        )
        raise UserRepositoryException from exception
    except (UserRepositoryException, Exception) as exception:
        artist_repository_logger.exception(
            f"Unexpected error removing song {song_name} from artist {artist_name} in database"
        )
        raise UserRepositoryException from exception
