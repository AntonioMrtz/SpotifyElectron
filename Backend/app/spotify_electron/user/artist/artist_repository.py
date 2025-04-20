"""Artist repository for managing persisted data"""

import app.spotify_electron.user.providers.user_collection_provider as provider
from app.logging.logging_constants import LOGGING_ARTIST_REPOSITORY
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.user.artist.artist_schema import (
    ArtistDAO,
    ArtistDocument,
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


async def get_artist(name: str) -> ArtistDAO:
    """Get artist by name

    Args:
        name: artist name

    Raises:
        ArtistNotFoundError: not found
        ArtistRepositoryError: unexpected error while getting artist

    Returns:
        the artist
    """
    try:
        collection = provider.get_artist_collection()
        artist = await collection.find_one({"name": name})

        validate_user_exists(artist)
        assert artist

        artist_dao = get_artist_dao_from_document(artist)

    except BaseUserNotFoundError as exception:
        raise ArtistNotFoundError from exception

    except Exception as exception:
        artist_repository_logger.exception(f"Error getting User {name} from database")
        raise ArtistRepositoryError from exception
    else:
        artist_repository_logger.info(f"Get Artist by name returned {artist_dao}")
        return artist_dao


async def create_artist(name: str, photo: str, password: bytes, current_date: str) -> None:
    """Create artist

    Args:
        name: artist name
        photo: artist photo
        password: artist hashed password
        current_date: formatted creation date

    Raises:
        ArtistRepositoryError: while creating Artist
    """
    try:
        artist = ArtistDocument(
            name=name,
            photo=photo,
            register_date=current_date,
            password=password,
            saved_playlists=[],
            playlists=[],
            playback_history=[],
            uploaded_songs=[],
        )
        collection = provider.get_artist_collection()
        result = await collection.insert_one(artist)

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


async def create_artist_from_user_dao(user: UserDAO) -> None:
    """Create artist from existing user data

    Args:
        user: Existing user data

    Raises:
        ArtistRepositoryError: while creating artist
    """
    try:
        artist = {
            "name": user.name,
            "photo": user.photo,
            "current_date": user.register_date,
            "password": user.password,
        }
        await create_artist(**artist)
        missing_fields = {
            "saved_playlists": user.saved_playlists if user.saved_playlists else [],
            "playlists": user.playlists if user.saved_playlists else [],
            "playback_history": user.playback_history if user.saved_playlists else [],
            "uploaded_songs": [],
        }

        collection = provider.get_artist_collection()
        result = await collection.update_one({"name": user.name}, {"$set": missing_fields})
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


async def get_all_artists() -> list[ArtistDAO]:
    """Get all artists

    Raises:
        ArtistRepositoryError: getting all artists

    Returns:
        a list with all artists
    """
    try:
        collection = provider.get_artist_collection()
        all_artists = collection.find()
        artists = [get_artist_dao_from_document(artist) async for artist in all_artists]
    except Exception as exception:
        artist_repository_logger.exception("Error getting all artists names from database")
        raise ArtistRepositoryError from exception
    else:
        artist_repository_logger.info("All artists names retrieved successfully")
        return artists


async def add_song_to_artist(artist_name: str, song_name: str) -> None:
    """Add song to artist

    Args:
        artist_name: artist name
        song_name: song name

    Raises:
        ArtistRepositoryError: adding song to artist
    """
    try:
        collection = provider.get_artist_collection()
        result = await collection.update_one(
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


async def delete_song_from_artist(artist_name: str, song_name: str) -> None:
    """Delete song from artist

    Args:
        artist_name: artist name
        song_name: song name

    Raises:
        ArtistRepositoryError: deleting song from artist
    """
    try:
        collection = provider.get_artist_collection()
        result = await collection.update_one(
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


async def get_artist_song_names(artist_name: str) -> list[str]:
    """Get artist song names

    Args:
        artist_name: artist name

    Returns:
        the artist uploaded song names
    """
    collection = provider.get_artist_collection()
    artist_data = await collection.find_one(
        {"name": artist_name}, {"uploaded_songs": 1, "_id": 0}
    )

    validate_user_exists(artist_data)
    assert artist_data

    return artist_data["uploaded_songs"]
