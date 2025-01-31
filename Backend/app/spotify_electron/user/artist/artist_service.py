"""
Artist service for handling business logic
"""

import app.auth.auth_service as auth_service
import app.spotify_electron.song.base_song_service as base_song_service
import app.spotify_electron.user.artist.artist_repository as artist_repository
import app.spotify_electron.user.artist.validations.artist_service_validations as artist_service_validations  # noqa: E501
import app.spotify_electron.user.base_user_repository as base_user_repository
import app.spotify_electron.user.providers.user_collection_provider as user_collection_provider
import app.spotify_electron.user.validations.base_user_service_validations as base_user_service_validations  # noqa: E501
from app.auth.auth_schema import UserUnauthorizedException
from app.logging.logging_constants import LOGGING_ARTIST_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.song.base_song_schema import (
    SongBadNameException,
    SongMetadataDTO,
    SongServiceException,
)
from app.spotify_electron.song.validations.base_song_service_validations import (
    validate_song_name_parameter,
)
from app.spotify_electron.user.artist.artist_schema import (
    ArtistBadNameException,
    ArtistDTO,
    ArtistNotFoundException,
    ArtistRepositoryException,
    ArtistServiceException,
    get_artist_dto_from_dao,
)
from app.spotify_electron.user.base_user_schema import (
    BaseUserAlreadyExistsException,
    BaseUserBadNameException,
    BaseUserNotFoundException,
)
from app.spotify_electron.utils.date.date_utils import get_current_iso8601_date

artist_service_logger = SpotifyElectronLogger(LOGGING_ARTIST_SERVICE).getLogger()


def add_song_to_artist(artist_name: str, song_name: str) -> None:
    """Add song to artist

    Args:
        artist_name (str): artist name
        song_name (str): song name

    Raises:
        ArtistBadNameException: artist invalid name
        ArtistNotFoundException: artist doesn't exists
        SongBadNameException: song invalid name
        ArtistServiceException: unexpected error adding song to artist
    """
    try:
        base_user_service_validations.validate_user_name_parameter(artist_name)
        validate_song_name_parameter(song_name)

        artist_service_validations.validate_user_should_be_artist(artist_name)

        artist_repository.add_song_to_artist(artist_name, song_name)

    except BaseUserAlreadyExistsException as exception:
        artist_service_logger.exception(f"Bad Artist Name Parameter: {artist_name}")
        raise ArtistBadNameException from exception
    except ArtistNotFoundException as exception:
        artist_service_logger.exception(f"Artist not found: {artist_name}")
        raise ArtistNotFoundException from exception
    except SongBadNameException as exception:
        artist_service_logger.exception(f"Bad Song Name Parameter: {song_name}")
        raise SongBadNameException from exception
    except UserUnauthorizedException as exception:
        artist_service_logger.exception(f"User {artist_name} is not Artist")
        raise UserUnauthorizedException from exception
    except ArtistRepositoryException as exception:
        artist_service_logger.exception(
            f"Unexpected error adding song {song_name} to artist {artist_name}"
        )
        raise ArtistServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist service adding song {song_name} "
            f"to artist {artist_name}"
        )
        raise ArtistServiceException from exception


def delete_song_from_artist(artist_name: str, song_name: str) -> None:
    """Remove song from artist

    Args:
        artist_name (str): artist name
        song_name (str): song name

    Raises:
        ArtistBadNameException: artist invalid name
        ArtistNotFoundException: artist doesn't exists
        SongBadNameException: song invalid name
        ArtistServiceException: unexpected error removing song from artist
    """
    try:
        base_user_service_validations.validate_user_name_parameter(artist_name)
        validate_song_name_parameter(song_name)

        artist_service_validations.validate_user_should_be_artist(artist_name)

        artist_repository.delete_song_from_artist(artist_name, song_name)
    except BaseUserAlreadyExistsException as exception:
        artist_service_logger.exception(f"Bad Artist Name Parameter: {artist_name}")
        raise ArtistBadNameException from exception
    except ArtistNotFoundException as exception:
        artist_service_logger.exception(f"Artist not found: {artist_name}")
        raise ArtistNotFoundException from exception
    except SongBadNameException as exception:
        artist_service_logger.exception(f"Bad Song Name Parameter: {song_name}")
        raise SongBadNameException from exception
    except UserUnauthorizedException as exception:
        artist_service_logger.exception(f"User {artist_name} is not Artist")
        raise UserUnauthorizedException from exception
    except ArtistRepositoryException as exception:  # noqa: F821
        artist_service_logger.exception(
            f"Unexpected error removing song {song_name} from artist {artist_name}"
        )
        raise ArtistServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist service removing song {song_name} "
            f"from artist {artist_name}"
        )
        raise ArtistServiceException from exception


def get_user(name: str) -> ArtistDTO:
    """Get artist from name

    Args:
        name (str): artist name

    Returns:
        ArtistDTO: the artist
    """
    return get_artist(name)


def get_artist(artist_name: str) -> ArtistDTO:
    """Get artist from name

    Args:
        artist_name (str): the artist name

    Raises:
        ArtistBadNameException: invalid user name
        ArtistNotFoundException: artist not found
        ArtistServiceException: unexpected error while getting artist

    Returns:
        ArtistDTO: the artist
    """
    try:
        base_user_service_validations.validate_user_name_parameter(artist_name)
        artist = artist_repository.get_user(artist_name)
        artist_dto = get_artist_dto_from_dao(artist)
    except BaseUserBadNameException as exception:
        artist_service_logger.exception(f"Bad Artist Name Parameter: {artist_name}")
        raise ArtistBadNameException from exception
    except ArtistNotFoundException as exception:
        artist_service_logger.exception(f"Artist not found: {artist_name}")
        raise ArtistNotFoundException from exception
    except ArtistRepositoryException as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Repository getting user: {artist_name}"
        )
        raise ArtistServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Service getting artist: {artist_name}"
        )
        raise ArtistServiceException from exception
    else:
        artist_service_logger.info(f"Artist {artist_name} retrieved successfully")
        return artist_dto


def create_artist(user_name: str, photo: str, password: str) -> None:
    """Create artist

    Args:
        user_name (str): artist name
        photo (str): artist photo
        password (str): artist password

    Raises:
        BaseUserAlreadyExistsException: if the artist already exists
        ArtistBadNameException: if the artist name is invalid
        ArtistServiceException: unexpected error while creating artist
    """
    try:
        base_user_service_validations.validate_user_name_parameter(user_name)
        base_user_service_validations.validate_user_should_not_exist(user_name)

        date = get_current_iso8601_date()
        photo = photo if "http" in photo else ""
        hashed_password = auth_service.hash_password(password)

        artist_repository.create_artist(
            name=user_name,
            photo=photo,
            current_date=date,
            password=hashed_password,
        )
        artist_service_logger.info(f"Artist {user_name} created successfully")
    except BaseUserAlreadyExistsException as exception:
        artist_service_logger.exception(f"Artist already exists: {user_name}")
        raise BaseUserAlreadyExistsException from exception
    except BaseUserBadNameException as exception:
        artist_service_logger.exception(f"Bad Artist Name Parameter: {user_name}")
        raise ArtistBadNameException from exception
    except ArtistRepositoryException as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Repository creating artist: {user_name}"
        )
        raise ArtistServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Service creating artist: {user_name}"
        )
        raise ArtistServiceException from exception


def get_all_artists() -> list[ArtistDTO]:
    """Get all artists

    Raises:
        ArtistServiceException: unexpected error getting all artists

    Returns:
        list[ArtistDTO]: the list of all artists
    """
    try:
        artists_dao = artist_repository.get_all_artists()
        artists_dto = [get_artist_dto_from_dao(artist_dao) for artist_dao in artists_dao]
    except ArtistRepositoryException as exception:
        artist_service_logger.exception(
            "Unexpected error in Artist Repository getting all artists"
        )
        raise ArtistServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            "Unexpected error in Artist Service getting all artists"
        )
        raise ArtistServiceException from exception
    else:
        artist_service_logger.info("All artists retrieved successfully")
        return artists_dto


# TODO obtain all users in same query
def get_artists(user_names: list[str]) -> list[ArtistDTO]:
    """Get artists from a list of names

    Args:
        user_names (list[str]): the list with the artist names to retrieve

    Raises:
        ArtistServiceException: unexpected error getting selected artists

    Returns:
        list[ArtistDTO]: the selected artists
    """
    try:
        artists: list[ArtistDTO] = []
        for user_name in user_names:
            artists.append(get_artist(user_name))

    except ArtistRepositoryException as exception:
        artist_service_logger.exception(
            f"Unexpected error in User Repository getting users {user_names}"
        )
        raise ArtistServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in User Service getting users {user_names}"
        )
        raise ArtistServiceException from exception
    else:
        artist_service_logger.info("All Users retrieved successfully")
        return artists


def search_by_name(name: str) -> list[ArtistDTO]:
    """Retrieve the artists than match the name

    Args:
        name (str): name to match

    Raises:
        ArtistServiceException: unexpected error searching artists that match a name

    Returns:
        list[ArtistDTO]: artists that match the name
    """
    try:
        matched_items_names = base_user_repository.search_by_name(
            name, user_collection_provider.get_artist_collection()
        )

        return get_artists(matched_items_names)
    except BaseUserNotFoundException as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Repository getting items by name {name}"
        )
        raise ArtistServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Service getting items by name {name}"
        )
        raise ArtistServiceException from exception


def does_artist_exists(user_name: str) -> bool:
    """Returns if artist exists

    Args:
    ----
        user_name (str): artist name

    Returns:
    -------
        bool: if the artist exists

    """
    return base_user_repository.check_user_exists(
        user_name, user_collection_provider.get_artist_collection()
    )


def get_artists_songs(artist_name: str) -> list[SongMetadataDTO]:
    """Get artists songs

    Args:
        artist_name (str): artist name

    Raises:
        SongBadNameException: song invalid name
        UserUnauthorizedException: user is not artist
        ArtistServiceException: unexpected error getting artist songs

    Returns:
        list[SongMetadataDTO]: the artist songs
    """
    try:
        validate_song_name_parameter(artist_name)
        artist_service_validations.validate_user_should_be_artist(artist_name)
        artist_song_names = artist_repository.get_artist_song_names(artist_name)
        artist_songs = base_song_service.get_songs_metadata(artist_song_names)
    except SongBadNameException as exception:
        artist_service_logger.exception(f"Bad Song name parameter in: {artist_song_names}")
        raise SongBadNameException from exception
    except UserUnauthorizedException as exception:
        artist_service_logger.exception(f"User {artist_name} is not Artist")
        raise UserUnauthorizedException from exception
    except SongServiceException as exception:
        artist_service_logger.exception(
            f"Unexpected error in Song Service songs from artist {artist_name}"
        )
        raise ArtistServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Service songs from artist {artist_name}"
        )
        raise ArtistServiceException from exception
    else:
        return artist_songs
