"""
Song service for handling business logic
"""

import app.spotify_electron.song.base_song_repository as base_song_repository
import app.spotify_electron.song.blob.song_repository as song_repository
import app.spotify_electron.user.artist.artist_service as artist_service
import app.spotify_electron.user.base_user_service as base_user_service
from app.auth.auth_schema import (
    TokenData,
    UserUnauthorizedException,
)
from app.logging.logging_constants import LOGGING_SONG_BLOB_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.genre.genre_schema import Genre, GenreNotValidException
from app.spotify_electron.song.aws.serverless_function.song_schema import (
    SongGetUrlStreamingException,
)
from app.spotify_electron.song.base_song_schema import (
    SongBadNameException,
    SongNotFoundException,
    SongRepositoryException,
    SongServiceException,
    SongUnAuthorizedException,
)
from app.spotify_electron.song.blob.song_schema import (
    SongDTO,
    get_song_dto_from_dao,
)
from app.spotify_electron.song.validations.base_song_service_validations import (
    validate_song_name_parameter,
    validate_song_should_exists,
    validate_song_should_not_exists,
)
from app.spotify_electron.user.artist.validations.artist_repository_validations import (
    validate_user_should_be_artist,
)
from app.spotify_electron.user.user.user_schema import (
    UserBadNameException,
    UserNotFoundException,
    UserServiceException,
)
from app.spotify_electron.user.validations.user_service_validations import (
    validate_user_name_parameter,
)
from app.spotify_electron.utils.audio_management.audio_management_utils import (
    EncodingFileException,
    get_song_duration_seconds,
)

song_service_logger = SpotifyElectronLogger(LOGGING_SONG_BLOB_SERVICE).getLogger()


def get_song(name: str) -> SongDTO:
    """Get song

    Args:
        name (str): song name

    Raises:
        SongBadNameException: invalid song name
        SongNotFoundException: song not found
        SongServiceException: unexpected error while getting song

    Returns:
        SongDTO: the song
    """
    try:
        validate_song_name_parameter(name)

        song_dao = song_repository.get_song(name)
        song_dto = get_song_dto_from_dao(song_dao)

    except SongBadNameException as exception:
        song_service_logger.exception(f"Bad Song Name Parameter : {name}")
        raise SongBadNameException from exception
    except SongNotFoundException as exception:
        song_service_logger.exception(f"Song not found : {name}")
        raise SongNotFoundException from exception
    except SongGetUrlStreamingException as exception:
        song_service_logger.exception(f"Error getting song streaming url for: {name}")
        raise SongServiceException from exception
    except SongRepositoryException as exception:
        song_service_logger.exception(
            f"Unexpected error in Song Repository getting song : {name}"
        )
        raise SongServiceException from exception
    except Exception as exception:
        song_service_logger.exception(
            f"Unexpected error in Song Service getting song : {name}"
        )
        raise SongServiceException from exception
    else:
        song_service_logger.info(f"Song {name} retrieved successfully")
        return song_dto


async def create_song(  # noqa: C901
    name: str, genre: Genre, photo: str, file: bytes, token: TokenData
) -> None:
    """Create song

    Args:
        name (str): song name
        genre (Genre): song genre
        photo (str): song photo
        file (bytes): song file
        token (TokenData): user token

    Raises:
        GenreNotValidException: invalid genre
        UserBadNameException: invalid user name
        UserNotFoundException: user doesnt exists
        EncodingFileException: error encoding file
        SongBadNameException: song bad name
        SongUnAuthorizedException: song created by unauthorized user
    """
    artist = token.username

    try:
        validate_song_name_parameter(name)
        validate_user_name_parameter(artist)
        Genre.check_valid_genre(genre.value)

        validate_song_should_not_exists(name)
        base_user_service.validate_user_should_exists(artist)

        validate_user_should_be_artist(artist)

        song_duration = get_song_duration_seconds(name, file)
        song_repository.create_song(
            name=name,
            artist=artist,
            photo=photo,
            duration=song_duration,
            genre=genre,
            file=file,
        )
        artist_service.add_song_artist(artist, name)
    except GenreNotValidException as exception:
        song_service_logger.exception(f"Bad genre provided {genre}")
        raise GenreNotValidException from exception
    except UserBadNameException as exception:
        song_service_logger.exception(f"Bad Artist Name Parameter : {artist}")
        raise UserBadNameException from exception
    except UserNotFoundException as exception:
        song_service_logger.exception(f"Artist {artist} not found")
        raise UserNotFoundException from exception
    except EncodingFileException as exception:
        song_service_logger.exception(f"Error encoding file with name {name}")
        raise EncodingFileException from exception
    except SongBadNameException as exception:
        song_service_logger.exception(f"Bad Song Name Parameter : {name}")
        raise SongBadNameException from exception
    except UserUnauthorizedException as exception:
        song_service_logger.exception(
            f"User {artist} cannot create song {name} because hes not artist"
        )
        raise SongUnAuthorizedException from exception
    except UserServiceException as exception:
        song_service_logger.exception(
            f"Unexpected error in User Service while creating song : {name}"
        )
        raise SongServiceException from exception
    except SongRepositoryException as exception:
        song_service_logger.exception(
            f"Unexpected error in Song Repository creating song : {name}"
        )
        raise SongServiceException from exception
    except Exception as exception:
        song_service_logger.exception(
            f"Unexpected error in Song Service creating song : {name}"
        )
        raise SongServiceException from exception


def delete_song(name: str) -> None:
    """Delete song

    Args:
        name (str): song name

    Raises:
        SongNotFoundException: song doesnt exists
        SongBadNameException: invalid song nae
        UserNotFoundException: artist doesnt exists
        SongServiceException: unexpected error deleting song
    """
    try:
        validate_song_name_parameter(name)
        validate_song_should_exists(name)
        artist_name = base_song_repository.get_artist_from_song(name=name)

        base_user_service.validate_user_should_exists(artist_name)

        artist_service.delete_song_from_artist(
            artist_name,
            name,
        )
        base_song_repository.delete_song(name)

    except SongNotFoundException as exception:
        song_service_logger.exception(f"Song not found : {name}")
        raise SongNotFoundException from exception
    except SongBadNameException as exception:
        song_service_logger.exception(f"Bad Song Name Parameter : {name}")
        raise SongBadNameException from exception
    except UserNotFoundException as exception:
        song_service_logger.exception(f"User {artist_name} not found")
        raise UserNotFoundException from exception
    except SongRepositoryException as exception:
        song_service_logger.exception(
            f"Unexpected error in Song Repository deleting song : {name}"
        )
        raise SongServiceException from exception
    except Exception as exception:
        song_service_logger.exception(
            f"Unexpected error in Song Service deleting song : {name}"
        )
        raise SongServiceException from exception
