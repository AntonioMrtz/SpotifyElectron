"""
Artist service for handling business logic
"""

import app.auth.auth_service as auth_service
import app.spotify_electron.song.base_song_service as base_song_service
import app.spotify_electron.user.artist.artist_repository as artist_repository
import app.spotify_electron.user.base_user_repository as base_user_repository
import app.spotify_electron.user.base_user_service as base_user_service
import app.spotify_electron.user.providers.user_collection_provider as user_collection_provider
from app.logging.logging_constants import LOGGING_ARTIST_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.song.base_song_schema import (
    SongBadNameException,
    SongServiceException,
)
from app.spotify_electron.song.validations.base_song_service_validations import (
    validate_song_name_parameter,
)
from app.spotify_electron.user.artist.artist_schema import (
    ArtistDTO,
    get_artist_dto_from_dao,
)
from app.spotify_electron.user.user.user_schema import (
    UserAlreadyExistsException,
    UserBadNameException,
    UserNotFoundException,
    UserRepositoryException,
    UserServiceException,
)
from app.spotify_electron.user.validations.user_service_validations import (
    validate_user_name_parameter,
)
from app.spotify_electron.utils.date.date_utils import get_current_iso8601_date

artist_service_logger = SpotifyElectronLogger(LOGGING_ARTIST_SERVICE).getLogger()


def add_song_artist(artist_name: str, song_name: str):
    """Add song to artist

    Args:
        artist_name (str): artist name
        song_name (str): song name

    Raises:
        UserBadNameException: user invalid name
        UserNotFoundException: user doesnt exists
        SongBadNameException: song invalid name
        UserServiceException: unexpected error adding song to artist
    """
    try:
        validate_user_name_parameter(artist_name)
        validate_song_name_parameter(song_name)

        base_user_service.validate_user_should_exists(artist_name)

        artist_repository.add_song_to_artist(artist_name, song_name)

    except UserBadNameException as exception:
        artist_service_logger.exception(f"Bad Artist Name Parameter : {artist_name}")
        raise UserBadNameException from exception
    except UserNotFoundException as exception:
        artist_service_logger.exception(f"Artist not found : {artist_name}")
        raise UserNotFoundException from exception
    except SongBadNameException as exception:
        artist_service_logger.exception(f"Bad Song Name Parameter : {song_name}")
        raise SongBadNameException from exception
    except UserRepositoryException as exception:
        artist_service_logger.exception(
            f"Unexpected error adding song {song_name} to artist {artist_name}"
        )
        raise UserServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist service adding song {song_name} "
            f"to artist {artist_name}"
        )
        raise UserServiceException from exception


def delete_song_from_artist(artist_name: str, song_name: str):
    """Remove song from artist

    Args:
        artist_name (str): artist name
        song_name (str): song name

    Raises:
        UserBadNameException: user invalid name
        UserNotFoundException: user doesnt exists
        SongBadNameException: song invalid name
        UserServiceException: unexpected error removing song from artist
    """
    try:
        validate_user_name_parameter(artist_name)
        validate_song_name_parameter(song_name)

        base_user_service.validate_user_should_exists(artist_name)

        artist_repository.delete_song_from_artist(artist_name, song_name)
    except UserBadNameException as exception:
        artist_service_logger.exception(f"Bad Artist Name Parameter : {artist_name}")
        raise UserBadNameException from exception
    except UserNotFoundException as exception:
        artist_service_logger.exception(f"Artist not found : {artist_name}")
        raise UserNotFoundException from exception
    except SongBadNameException as exception:
        artist_service_logger.exception(f"Bad Song Name Parameter : {song_name}")
        raise SongBadNameException from exception
    except UserRepositoryException as exception:
        artist_service_logger.exception(
            f"Unexpected error removing song {song_name} from artist {artist_name}"
        )
        raise UserServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist service removing song {song_name} "
            f"from artist {artist_name}"
        )
        raise UserServiceException from exception


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
        UserBadNameException: invalid user name
        UserNotFoundException: artist not found
        UserServiceException: unexpected error while getting artist

    Returns:
        ArtistDTO: the artist
    """
    try:
        validate_user_name_parameter(artist_name)
        artist = artist_repository.get_user(artist_name)
        artist_dto = get_artist_dto_from_dao(artist)
    except UserBadNameException as exception:
        artist_service_logger.exception(f"Bad Artist Name Parameter : {artist_name}")
        raise UserBadNameException from exception
    except UserNotFoundException as exception:
        artist_service_logger.exception(f"Artist not found : {artist_name}")
        raise UserNotFoundException from exception
    except UserRepositoryException as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Repository getting user : {artist_name}"
        )
        raise UserServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Service getting artist : {artist_name}"
        )
        raise UserServiceException from exception
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
        UserAlreadyExistsException: if the artist already exists
        UserBadNameException: if the artist name is invalid
        UserServiceException: unexpected error while creating artist
    """
    try:
        validate_user_name_parameter(user_name)
        base_user_service.validate_user_should_not_exist(user_name)

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
    except UserAlreadyExistsException as exception:
        artist_service_logger.exception(f"Artist already exists : {user_name}")
        raise UserAlreadyExistsException from exception
    except UserBadNameException as exception:
        artist_service_logger.exception(f"Bad Artist Name Parameter : {user_name}")
        raise UserBadNameException from exception
    except UserRepositoryException as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Repository creating artist : {user_name}"
        )
        raise UserServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Service creating artist : {user_name}"
        )
        raise UserServiceException from exception


def get_all_artists() -> list[ArtistDTO]:
    """Get all artists

    Raises:
        UserServiceException: unexpected error getting all artists

    Returns:
        list[ArtistDTO]: the list of all artists
    """
    try:
        artists_dao = artist_repository.get_all_artists()
        artists_dto = [get_artist_dto_from_dao(artist_dao) for artist_dao in artists_dao]
    except UserRepositoryException as exception:
        artist_service_logger.exception(
            "Unexpected error in Artist Repository getting all artists"
        )
        raise UserServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            "Unexpected error in Artist Service getting all artists"
        )
        raise UserServiceException from exception
    else:
        artist_service_logger.info("All artists retrieved successfully")
        return artists_dto


def get_streams_artist(user_name: str) -> int:
    """Get artist songs total streams

    Args:
        user_name (str): artist name

    Raises:
        UserNotFoundException: artist doesnt exists
        UserBadNameException: artist bad name
        UserServiceException: unexpected error getting artist total streams

    Returns:
        int: the total for all artist songs
    """
    try:
        validate_user_name_parameter(user_name)
        base_user_service.validate_user_should_exists(user_name)

        return base_song_service.get_artist_streams(user_name)
    except UserNotFoundException as exception:
        artist_service_logger.exception(f"Artist not found : {user_name}")
        raise UserNotFoundException from exception
    except UserBadNameException as exception:
        artist_service_logger.exception(f"Bad Artist Name Parameter : {user_name}")
        raise UserBadNameException from exception
    except UserRepositoryException as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Repository getting artist : {user_name}"
        )
        raise UserServiceException from exception
    except SongServiceException as exception:
        artist_service_logger.exception(
            f"Unexpected error in Song Service getting artist : {user_name}"
        )
        raise UserServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Service getting artist : {user_name}"
        )
        raise UserServiceException from exception


# TODO obtain all users in same query
def get_artists(user_names: list[str]) -> list[ArtistDTO]:
    """Get artists from a list of names

    Args:
        user_names (list[str]): the list with the artist names to retrieve

    Raises:
        UserServiceException: if unexpected error getting selected artists

    Returns:
        list[ArtistDTO]: the selected artists
    """
    try:
        artists: list[ArtistDTO] = []
        for user_name in user_names:
            artists.append(get_artist(user_name))

    except UserRepositoryException as exception:
        artist_service_logger.exception(
            f"Unexpected error in User Repository getting users {user_names}"
        )
        raise UserServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in User Service getting users {user_names}"
        )
        raise UserServiceException from exception
    else:
        artist_service_logger.info("All Users retrieved successfully")
        return artists


def search_by_name(name: str) -> list[ArtistDTO]:
    """Retrieve the artists than match the name

    Args:
        name (str): name to match

    Raises:
        UserServiceException: if unexpected error searching artists that match a name

    Returns:
        list[ArtistDTO]: artists that match the name
    """
    try:
        matched_items_names = base_user_repository.search_by_name(
            name, user_collection_provider.get_artist_collection()
        )

        return get_artists(matched_items_names)
    except UserRepositoryException as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Repository getting items by name {name}"
        )
        raise UserServiceException from exception
    except Exception as exception:
        artist_service_logger.exception(
            f"Unexpected error in Artist Service getting items by name {name}"
        )
        raise UserServiceException from exception


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
