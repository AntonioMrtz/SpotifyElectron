"""
Artist service for handling business logic
"""

from asyncio import gather

import app.auth.auth_service as auth_service
import app.spotify_electron.song.base_song_service as base_song_service
import app.spotify_electron.user.artist.artist_repository as artist_repository
import app.spotify_electron.user.artist.validations.artist_service_validations as artist_service_validations  # noqa: E501
import app.spotify_electron.user.base_user_repository as base_user_repository
import app.spotify_electron.user.providers.user_collection_provider as provider
import app.spotify_electron.user.validations.base_user_service_validations as base_user_service_validations  # noqa: E501
from app.auth.auth_schema import UserUnauthorizedError
from app.logging.logging_constants import LOGGING_ARTIST_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.song.base_song_schema import (
    SongBadNameError,
    SongMetadataDTO,
    SongServiceError,
)
from app.spotify_electron.song.validations.base_song_service_validations import (
    validate_song_name_parameter,
)
from app.spotify_electron.user.artist.artist_schema import (
    ArtistAlreadyExistsError,
    ArtistBadNameError,
    ArtistDTO,
    ArtistNotFoundError,
    ArtistRepositoryError,
    ArtistServiceError,
    get_artist_dto_from_dao,
)
from app.spotify_electron.user.base_user_schema import (
    BaseUserAlreadyExistsError,
    BaseUserBadNameError,
    BaseUserNotFoundError,
)
from app.spotify_electron.user.user.user_schema import UserDAO
from app.spotify_electron.utils.date.date_utils import get_current_iso8601_date

artist_service_logger = SpotifyElectronLogger(LOGGING_ARTIST_SERVICE).get_logger()


async def get_user(name: str) -> ArtistDTO:
    """Get artist from name

    Args:
        name (str): artist name

    Returns:
        ArtistDTO: the artist
    """
    return await get_artist(name)


async def get_artist(artist_name: str) -> ArtistDTO:
    """Get artist from name

    Args:
        artist_name (str): the artist name

    Raises:
        ArtistBadNameError: invalid user name
        ArtistNotFoundError: artist not found
        ArtistServiceError: unexpected error while getting artist

    Returns:
        ArtistDTO: the artist
    """
    try:
        await base_user_service_validations.validate_user_name_parameter(artist_name)

        artist = await artist_repository.get_artist(artist_name)
        total_streams = await base_song_service.get_artist_total_streams(artist_name)
        artist.total_streams = total_streams

        artist_dto = get_artist_dto_from_dao(artist)
    except BaseUserBadNameError as exception:
        artist_service_logger.exception(f"Bad Artist Name Parameter: {artist_name}")
        raise ArtistBadNameError from exception
    except ArtistNotFoundError as exception:
        artist_service_logger.exception(f"Artist not found: {artist_name}")
        raise ArtistNotFoundError from exception
    except ArtistRepositoryError as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Repository getting user: {artist_name}"
        )
        raise ArtistServiceError from exception
    except SongServiceError as exception:
        artist_service_logger.exception(
            f"Unexpected error in Song Service getting total streams for artist: {artist_name}"
        )
        raise ArtistServiceError from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Service getting artist: {artist_name}"
        )
        raise ArtistServiceError from exception
    else:
        artist_service_logger.info(f"Artist {artist_name} retrieved successfully")
        return artist_dto


async def create_artist(user_name: str, photo: str, password: str) -> None:
    """Create artist

    Args:
        user_name (str): artist name
        photo (str): artist photo
        password (str): artist password

    Raises:
        BaseUserAlreadyExistsError: if the artist already exists
        ArtistBadNameError: if the artist name is invalid
        ArtistServiceError: unexpected error while creating artist
    """
    try:
        await base_user_service_validations.validate_user_name_parameter(user_name)
        await base_user_service_validations.validate_user_should_not_exist(user_name)

        date = get_current_iso8601_date()
        photo = photo if "http" in photo else ""
        hashed_password = auth_service.hash_password(password)

        await artist_repository.create_artist(
            name=user_name,
            photo=photo,
            current_date=date,
            password=hashed_password,
        )
        artist_service_logger.info(f"Artist {user_name} created successfully")
    except BaseUserAlreadyExistsError as exception:
        artist_service_logger.exception(f"Artist already exists: {user_name}")
        raise BaseUserAlreadyExistsError from exception
    except BaseUserBadNameError as exception:
        artist_service_logger.exception(f"Bad Artist Name Parameter: {user_name}")
        raise ArtistBadNameError from exception
    except ArtistRepositoryError as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Repository creating artist: {user_name}"
        )
        raise ArtistServiceError from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Service creating artist: {user_name}"
        )
        raise ArtistServiceError from exception


async def create_artist_from_user(user: UserDAO) -> None:
    """Create an Artist from an User object with existing data.

    Args:
        user (UserDAO): User data access object containing user information

    Raises:
        ArtistAlreadyExistsError: If artist already exists
        ArtistServiceError: If creation fails
    """
    try:
        await artist_service_validations.validate_artist_should_not_exist(user.name)
        await artist_repository.create_artist_from_user_dao(user)
    except ArtistAlreadyExistsError as exception:
        artist_service_logger.exception(
            f"The User with name {user.name} is already exists as Artist"
        )
        raise ArtistAlreadyExistsError from exception
    except ArtistRepositoryError as exception:
        artist_service_logger.exception(
            f"Repository error creating artist from User: {user.name}"
        )
        raise ArtistServiceError from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error creating artist from User: {user.name}"
        )
        raise ArtistServiceError from exception


async def get_all_artists() -> list[ArtistDTO]:
    """Get all artists

    Raises:
        ArtistServiceError: unexpected error getting all artists

    Returns:
        list[ArtistDTO]: the list of all artists
    """
    try:
        artists_dao = await artist_repository.get_all_artists()

        total_streams_list = await gather(
            *[
                base_song_service.get_artist_total_streams(artist.name)
                for artist in artists_dao
            ]
        )
        for artist_dao, total_streams in zip(artists_dao, total_streams_list):
            artist_dao.total_streams = total_streams

        artists_dto = [get_artist_dto_from_dao(artist_dao) for artist_dao in artists_dao]
    except ArtistRepositoryError as exception:
        artist_service_logger.exception(
            "Unexpected error in Artist Repository getting all artists"
        )
        raise ArtistServiceError from exception
    except Exception as exception:
        artist_service_logger.exception(
            "Unexpected error in Artist Service getting all artists"
        )
        raise ArtistServiceError from exception
    else:
        artist_service_logger.info("All artists retrieved successfully")
        return artists_dto


# TODO obtain all users in same query
async def get_artists(user_names: list[str]) -> list[ArtistDTO]:
    """Get artists from a list of names

    Args:
        user_names (list[str]): the list with the artist names to retrieve

    Raises:
        ArtistServiceError: unexpected error getting selected artists

    Returns:
        list[ArtistDTO]: the selected artists
    """
    try:
        artists: list[ArtistDTO] = []
        for user_name in user_names:
            artists.append(await get_artist(user_name))

    except ArtistRepositoryError as exception:
        artist_service_logger.exception(
            f"Unexpected error in User Repository getting users {user_names}"
        )
        raise ArtistServiceError from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in User Service getting users {user_names}"
        )
        raise ArtistServiceError from exception
    else:
        artist_service_logger.info("All Users retrieved successfully")
        return artists


async def search_by_name(name: str) -> list[ArtistDTO]:
    """Retrieve the artists than match the name

    Args:
        name (str): name to match

    Raises:
        ArtistServiceError: unexpected error searching artists that match a name

    Returns:
        list[ArtistDTO]: artists that match the name
    """
    try:
        artist_collection = provider.get_artist_collection()
        matched_items_names = await base_user_repository.search_by_name(
            name, artist_collection
        )

        return await get_artists(matched_items_names)
    except BaseUserNotFoundError as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Repository getting items by name {name}"
        )
        raise ArtistServiceError from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Service getting items by name {name}"
        )
        raise ArtistServiceError from exception


async def does_artist_exists(user_name: str) -> bool:
    """Returns if artist exists

    Args:
    ----
        user_name (str): artist name

    Returns:
    -------
        bool: if the artist exists

    """
    user_collection = provider.get_artist_collection()
    return await base_user_repository.check_user_exists(user_name, user_collection)


async def get_artists_songs(artist_name: str) -> list[SongMetadataDTO]:
    """Get artists songs

    Args:
        artist_name (str): artist name

    Raises:
        SongBadNameError: song invalid name
        UserUnauthorizedError: user is not artist
        ArtistServiceError: unexpected error getting artist songs

    Returns:
        list[SongMetadataDTO]: the artist songs
    """
    try:
        validate_song_name_parameter(artist_name)
        await artist_service_validations.validate_user_should_be_artist(artist_name)

        artist_song_names = await artist_repository.get_artist_song_names(artist_name)
        artist_songs = await base_song_service.get_songs_metadata(artist_song_names)
    except SongBadNameError as exception:
        artist_service_logger.exception(f"Bad Song name parameter in: {artist_song_names}")
        raise SongBadNameError from exception
    except UserUnauthorizedError as exception:
        artist_service_logger.exception(f"User {artist_name} is not Artist")
        raise UserUnauthorizedError from exception
    except SongServiceError as exception:
        artist_service_logger.exception(
            f"Unexpected error in Song Service songs from artist {artist_name}"
        )
        raise ArtistServiceError from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Service songs from artist {artist_name}"
        )
        raise ArtistServiceError from exception
    else:
        return artist_songs


async def add_song_to_artist(artist_name: str, song_name: str) -> None:
    """Add song to artist

    Args:
        artist_name (str): artist name
        song_name (str): song name

    Raises:
        ArtistBadNameError: artist invalid name
        ArtistNotFoundError: artist doesn't exists
        UserUnauthorizedError: user is not artist
        SongBadNameError: song invalid name
        ArtistServiceError: unexpected error adding song to artist
    """
    try:
        await base_user_service_validations.validate_user_name_parameter(artist_name)
        validate_song_name_parameter(song_name)

        await artist_service_validations.validate_user_should_be_artist(artist_name)

        await artist_repository.add_song_to_artist(artist_name, song_name)

    except BaseUserAlreadyExistsError as exception:
        artist_service_logger.exception(f"Bad Artist Name Parameter: {artist_name}")
        raise ArtistBadNameError from exception
    except ArtistNotFoundError as exception:
        artist_service_logger.exception(f"Artist not found: {artist_name}")
        raise ArtistNotFoundError from exception
    except SongBadNameError as exception:
        artist_service_logger.exception(f"Bad Song Name Parameter: {song_name}")
        raise SongBadNameError from exception
    except UserUnauthorizedError as exception:
        artist_service_logger.exception(f"User {artist_name} is not Artist")
        raise UserUnauthorizedError from exception
    except ArtistRepositoryError as exception:
        artist_service_logger.exception(
            f"Unexpected error adding song {song_name} to artist {artist_name}"
        )
        raise ArtistServiceError from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist service adding song {song_name} "
            f"to artist {artist_name}"
        )
        raise ArtistServiceError from exception


async def delete_song_from_artist(artist_name: str, song_name: str) -> None:
    """Remove song from artist

    Args:
        artist_name (str): artist name
        song_name (str): song name

    Raises:
        ArtistBadNameError: artist invalid name
        ArtistNotFoundError: artist doesn't exists
        SongBadNameError: song invalid name
        UserUnauthorizedError: user is not artist
        ArtistServiceError: unexpected error removing song from artist
    """
    try:
        await base_user_service_validations.validate_user_name_parameter(artist_name)
        validate_song_name_parameter(song_name)

        await artist_service_validations.validate_user_should_be_artist(artist_name)

        await artist_repository.delete_song_from_artist(artist_name, song_name)
    except BaseUserAlreadyExistsError as exception:
        artist_service_logger.exception(f"Bad Artist Name Parameter: {artist_name}")
        raise ArtistBadNameError from exception
    except ArtistNotFoundError as exception:
        artist_service_logger.exception(f"Artist not found: {artist_name}")
        raise ArtistNotFoundError from exception
    except SongBadNameError as exception:
        artist_service_logger.exception(f"Bad Song Name Parameter: {song_name}")
        raise SongBadNameError from exception
    except UserUnauthorizedError as exception:
        artist_service_logger.exception(f"User {artist_name} is not Artist")
        raise UserUnauthorizedError from exception
    except ArtistRepositoryError as exception:  # noqa: F821
        artist_service_logger.exception(
            f"Unexpected error removing song {song_name} from artist {artist_name}"
        )
        raise ArtistServiceError from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist service removing song {song_name} "
            f"from artist {artist_name}"
        )
        raise ArtistServiceError from exception
