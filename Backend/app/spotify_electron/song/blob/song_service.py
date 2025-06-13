"""Song service for handling business logic"""

import app.spotify_electron.song.base_song_repository as base_song_repository
import app.spotify_electron.song.blob.song_repository as song_repository
import app.spotify_electron.user.artist.artist_service as artist_service
import app.spotify_electron.user.validations.base_user_service_validations as base_user_service_validations  # noqa: E501
from app.auth.auth_schema import (
    TokenData,
    UserUnauthorizedError,
)
from app.logging.logging_constants import LOGGING_SONG_BLOB_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.genre.genre_schema import Genre, GenreNotValidError
from app.spotify_electron.song.base_song_schema import (
    SongAlreadyExistsError,
    SongBadNameError,
    SongNotFoundError,
    SongRepositoryError,
    SongServiceError,
)
from app.spotify_electron.song.blob.song_schema import (
    SongDataNotFoundError,
    SongDTO,
    get_song_dto_from_dao,
)
from app.spotify_electron.song.serverless.song_schema import (
    SongGetUrlStreamingError,
)
from app.spotify_electron.song.validations.base_song_service_validations import (
    validate_song_name_parameter,
    validate_song_should_exists,
    validate_song_should_not_exists,
)
from app.spotify_electron.user.artist.validations.artist_service_validations import (
    validate_user_should_be_artist,
)
from app.spotify_electron.user.user.user_schema import (
    UserBadNameError,
    UserNotFoundError,
    UserServiceError,
)
from app.spotify_electron.utils.audio_management.audio_management_utils import (
    EncodingFileError,
    get_song_duration_seconds,
)

song_service_logger = SpotifyElectronLogger(LOGGING_SONG_BLOB_SERVICE).get_logger()


async def get_song(name: str) -> SongDTO:
    """Get song

    Args:
        name: song name

    Raises:
        SongBadNameError: name
        SongNotFoundError: song not found
        SongServiceError: unexpected error while getting song

    Returns:
        the song
    """
    try:
        validate_song_name_parameter(name)

        song_dao = await song_repository.get_song(name)
        song_dto = get_song_dto_from_dao(song_dao, song_dao.url)

    except SongBadNameError as exception:
        song_service_logger.exception(f"Bad Song Name Parameter: {name}")
        raise SongBadNameError from exception
    except SongNotFoundError as exception:
        song_service_logger.exception(f"Song not found: {name}")
        raise SongNotFoundError from exception
    except SongGetUrlStreamingError as exception:
        song_service_logger.exception(f"Error getting song streaming url for: {name}")
        raise SongServiceError from exception
    except SongRepositoryError as exception:
        song_service_logger.exception(
            f"Unexpected error in Song Repository getting song: {name}"
        )
        raise SongServiceError from exception
    except Exception as exception:
        song_service_logger.exception(f"Unexpected error in Song Service getting song: {name}")
        raise SongServiceError from exception
    else:
        song_service_logger.info(f"Song {name} retrieved successfully")
        return song_dto


async def create_song(  # noqa: C901
    name: str, genre: Genre, photo: str, file: bytes, token: TokenData
) -> None:
    """Create song

    Args:
        name: song name
        genre: song genre
        photo: song photo
        file: song file
        token: user token

    Raises:
        GenreNotValidError:
        UserBadNameError: invalid user name
        UserNotFoundError: user doesn't exists
        EncodingFileError: error encoding file
        SongBadNameError: song bad name
        UserUnauthorizedError: unauthorized user for creating song
        SongAlreadyExistsError: song already exists
        SongServiceError: unexpected error while creating song
    """
    artist = token.username

    try:
        validate_song_name_parameter(name)
        await base_user_service_validations.validate_user_name_parameter(artist)
        Genre.validate_genre(genre.value)

        await validate_song_should_not_exists(name)
        await validate_user_should_be_artist(artist)

        song_duration = get_song_duration_seconds(name, file)
        await song_repository.create_song(
            name=name,
            artist=artist,
            photo=photo,
            seconds_duration=song_duration,
            genre=genre,
            file=file,
        )
        await artist_service.add_song_to_artist(artist, name)
    except GenreNotValidError as exception:
        song_service_logger.exception(f"Bad genre provided {genre}")
        raise GenreNotValidError from exception
    except UserBadNameError as exception:
        song_service_logger.exception(f"Bad Artist Name Parameter: {artist}")
        raise UserBadNameError from exception
    except UserNotFoundError as exception:
        song_service_logger.exception(f"Artist {artist} not found")
        raise UserNotFoundError from exception
    except EncodingFileError as exception:
        song_service_logger.exception(f"Error encoding file with name {name}")
        raise EncodingFileError from exception
    except SongBadNameError as exception:
        song_service_logger.exception(f"Bad Song Name Parameter: {name}")
        raise SongBadNameError from exception
    except SongAlreadyExistsError as exception:
        song_service_logger.exception(f"Song already exists: {name}")
        raise SongAlreadyExistsError from exception
    except UserUnauthorizedError as exception:
        song_service_logger.exception(
            f"User {artist} cannot create song {name} because hes not artist"
        )
        raise UserUnauthorizedError from exception
    except UserServiceError as exception:
        song_service_logger.exception(
            f"Unexpected error in User Service while creating song: {name}"
        )
        raise SongServiceError from exception
    except SongRepositoryError as exception:
        song_service_logger.exception(
            f"Unexpected error in Song Repository creating song: {name}"
        )
        raise SongServiceError from exception
    except Exception as exception:
        song_service_logger.exception(
            f"Unexpected error in Song Service creating song: {name}"
        )
        raise SongServiceError from exception


async def delete_song(name: str) -> None:
    """Delete song

    Args:
        name: song name

    Raises:
        SongBadNameError: name
        SongNotFoundError: song doesn't exists
        UserNotFoundError: artist doesn't exists
        SongServiceError: unexpected error deleting song
    """
    try:
        validate_song_name_parameter(name)
        await validate_song_should_exists(name)
        artist_name = await base_song_repository.get_artist_from_song(name=name)

        await base_user_service_validations.validate_user_should_exists(artist_name)

        await artist_service.delete_song_from_artist(
            artist_name,
            name,
        )
        await base_song_repository.delete_song(name)

    except SongBadNameError as exception:
        song_service_logger.exception(f"Bad Song Name Parameter: {name}")
        raise SongBadNameError from exception
    except SongNotFoundError as exception:
        song_service_logger.exception(f"Song not found: {name}")
        raise SongNotFoundError from exception
    except UserNotFoundError as exception:
        song_service_logger.exception(f"User {artist_name} not found")
        raise UserNotFoundError from exception
    except UserUnauthorizedError as exception:
        song_service_logger.exception(
            f"User {artist_name} cannot have song {name} removed because he's not an artist"
        )
        raise SongServiceError from exception
    except SongRepositoryError as exception:
        song_service_logger.exception(
            f"Unexpected error in Song Repository deleting song: {name}"
        )
        raise SongServiceError from exception
    except Exception as exception:
        song_service_logger.exception(
            f"Unexpected error in Song Service deleting song: {name}"
        )
        raise SongServiceError from exception


async def get_song_data(name: str) -> bytes:
    """Get song data

    Args:
        name: song name

    Raises:
        SongBadNameError: name
        SongNotFoundError: song not found
        SongDataNotFoundError: song data doesn't exists
        SongServiceError: unexpected error getting song data

    Returns:
        song data
    """
    try:
        validate_song_name_parameter(name)
        await validate_song_should_exists(name)

        song_data = await song_repository.get_song_data(name)
        read_song_data = await song_data.read()
    except SongBadNameError as exception:
        song_service_logger.exception(f"Bad Song Name Parameter: {name}")
        raise SongBadNameError from exception
    except SongNotFoundError as exception:
        song_service_logger.exception(f"Song not found: {name}")
        raise SongNotFoundError from exception
    except SongDataNotFoundError as exception:
        song_service_logger.exception(f"Song data not found: {name}")
        raise SongDataNotFoundError from exception
    except SongRepositoryError as exception:
        song_service_logger.exception(
            f"Unexpected error in Song Repository getting song data: {name}"
        )
        raise SongServiceError from exception
    except Exception as exception:
        song_service_logger.exception(
            f"Unexpected error in Song Service getting song data: {name}"
        )
        raise SongServiceError from exception
    else:
        song_service_logger.info("Song data retrieved succesfully")
        return read_song_data
