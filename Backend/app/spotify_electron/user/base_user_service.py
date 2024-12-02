"""
Base User service for handling bussiness logic
Redirects to the specific user type service for non common logic
"""

import app.auth.auth_service as auth_service
import app.spotify_electron.playlist.playlist_service as playlist_service
import app.spotify_electron.song.base_song_service as base_song_service
import app.spotify_electron.user.artist.artist_service as artist_service
import app.spotify_electron.user.base_user_repository as base_user_repository
import app.spotify_electron.user.providers.user_collection_provider as user_collection_provider
import app.spotify_electron.user.providers.user_service_provider as user_service_provider
import app.spotify_electron.user.validations.base_user_service_validations as base_user_service_validations  # noqa: E501
from app.auth.auth_schema import (
    TokenData,
    UserUnauthorizedException,
)
from app.logging.logging_constants import LOGGING_BASE_USERS_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.playlist.playlist_schema import (
    PlaylistBadNameException,
    PlaylistDTO,
    PlaylistNotFoundException,
    PlaylistServiceException,
)
from app.spotify_electron.playlist.validations.playlist_service_validations import (
    validate_playlist_name_parameter,
    validate_playlist_should_exists,
)
from app.spotify_electron.song.base_song_schema import (
    SongBadNameException,
    SongMetadataDTO,
    SongNotFoundException,
)
from app.spotify_electron.song.validations.base_song_service_validations import (
    validate_song_name_parameter,
    validate_song_should_exists,
)
from app.spotify_electron.user.base_user_schema import (
    BaseUserBadNameException,
    BaseUserDTO,
    BaseUserNotFoundException,
    BaseUserRepositoryException,
    BaseUserServiceException,
)
from app.spotify_electron.user.user.user_schema import UserType
from app.spotify_electron.utils.validations.validation_utils import validate_parameter

base_users_service_logger = SpotifyElectronLogger(LOGGING_BASE_USERS_SERVICE).getLogger()


# TODO not hardcoded
MAX_NUMBER_PLAYBACK_HISTORY_SONGS = 5


def get_user_type(user_name: str) -> UserType:
    """Get user type

    Args:
        user_name (str): user name

    Returns:
        UserType: the user type/role
    """
    validate_parameter(user_name)
    base_user_service_validations.validate_user_should_exists(user_name)

    if artist_service.does_artist_exists(user_name):
        return UserType.ARTIST
    return UserType.USER


def get_user(user_name: str) -> BaseUserDTO:
    """Returns the user

    Args:
        user_name (str): the user name

    Returns:
        User: the user
    """
    return user_service_provider.get_user_service(user_name).get_user(user_name)


def delete_user(user_name: str) -> None:
    """Delete user

    Args:
        user_name (str): user name

    Raises:
        BaseUserBadNameException: invalid user name parameter
        BaseUserNotFoundException: user not found
        BaseUserServiceException: unexpected error while deleting user
    """
    try:
        base_user_service_validations.validate_user_name_parameter(user_name)
        base_user_service_validations.validate_user_should_exists(user_name)
        collection = user_collection_provider.get_user_associated_collection(user_name)
        base_user_repository.delete_user(user_name, collection)
    except BaseUserBadNameException as exception:
        base_users_service_logger.exception(f"Bad user Parameter: {user_name}")
        raise BaseUserBadNameException from exception
    except BaseUserNotFoundException as exception:
        base_users_service_logger.exception(f"User not found: {user_name}")
        raise BaseUserNotFoundException from exception
    except BaseUserRepositoryException as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Repository deleting user: {user_name}"
        )
        raise BaseUserServiceException from exception
    except Exception as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Service deleting user: {user_name}"
        )
        raise BaseUserServiceException from exception
    else:
        base_users_service_logger.info(f"User {user_name} deleted")


def get_user_password(user_name: str) -> bytes:
    """Get user hashed password

    Args:
        user_name (str): the user name

    Raises:
        BaseUserServiceException: unexpected error while getting user password

    Returns:
        bytes: the hashed password
    """
    try:
        collection = user_collection_provider.get_user_associated_collection(user_name)
        password = base_user_repository.get_user_password(user_name, collection)
    except BaseUserRepositoryException as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Repository getting password from user: {user_name}"
        )
        raise BaseUserServiceException from exception
    except Exception as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Service gettiing password from user: {user_name}"
        )
        raise BaseUserServiceException from exception
    else:
        base_users_service_logger.info(f"Password obtained for User: {user_name}")
        return password


def add_playback_history(user_name: str, song_name: str, token: TokenData) -> None:
    """Add playback history to user

    Args:
        user_name (str): user name
        song_name (str): song name to add
        token (TokenData): token data from user

    Raises:
        BaseUserBadNameException: invalid user name
        BaseUserNotFoundException: user doesn't exists
        SongBadNameException: invalid song name
        UserUnauthorizedException: user cannot modify playback history that \
            is not created by him
        SongNotFoundException: song doesn't exists
        BaseUserServiceException: unexpected error adding playback history to user
    """
    try:
        base_user_service_validations.validate_user_name_parameter(user_name)
        validate_song_name_parameter(song_name)
        auth_service.validate_jwt_user_matches_user(token, user_name)

        base_user_service_validations.validate_user_should_exists(user_name)
        validate_song_should_exists(song_name)

        base_user_repository.add_playback_history(
            user_name=user_name,
            song=song_name,
            max_number_playback_history_songs=MAX_NUMBER_PLAYBACK_HISTORY_SONGS,
            collection=user_collection_provider.get_user_associated_collection(user_name),
        )
    except BaseUserBadNameException as exception:
        base_users_service_logger.exception(f"Bad User Parameter: {user_name}")
        raise BaseUserBadNameException from exception
    except BaseUserNotFoundException as exception:
        base_users_service_logger.exception(f"User not found: {user_name}")
        raise BaseUserNotFoundException from exception
    except SongBadNameException as exception:
        base_users_service_logger.exception(f"Bad Song Name Parameter: {song_name}")
        raise SongBadNameException from exception
    except UserUnauthorizedException as exception:
        base_users_service_logger.exception(
            f"Unathorized user {user_name} for adding playback songs"
        )
        raise UserUnauthorizedException from exception
    except SongNotFoundException as exception:
        base_users_service_logger.exception(f"Song not found: {song_name}")
        raise SongNotFoundException from exception
    except BaseUserRepositoryException as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Repository adding song {song_name} "
            f"to user {user_name} playback history"
        )
        raise BaseUserServiceException from exception
    except Exception as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Service adding song {song_name} "
            f"to user {user_name} playback history"
        )
        raise BaseUserServiceException from exception
    else:
        base_users_service_logger.info(
            f"Song {song_name} added to User {user_name} playback history"
        )


def add_saved_playlist(user_name: str, playlist_name: str, token: TokenData) -> None:
    """Add saved playlist to user

    Args:
        user_name (str): user name
        playlist_name (str): playlist name
        token (TokenData): user token data

    Raises:
        BaseUserBadNameException: invalid user name
        PlaylistBadNameException: invalid playlist name
        UserUnauthorizedException: user cannot access a playlist that is not created by him
        PlaylistNotFoundException: playlist doesn't exists
        BaseUserServiceException: unexpected error adding saved playlist to user
    """
    try:
        base_user_service_validations.validate_user_name_parameter(user_name)
        validate_playlist_name_parameter(playlist_name)
        auth_service.validate_jwt_user_matches_user(token, user_name)
        base_user_service_validations.validate_user_should_exists(user_name)
        validate_playlist_should_exists(playlist_name)

        base_user_repository.add_saved_playlist(
            user_name=user_name,
            playlist_name=playlist_name,
            collection=user_collection_provider.get_user_associated_collection(user_name),
        )
    except BaseUserBadNameException as exception:
        base_users_service_logger.exception(f"Bad User Parameter: {user_name}")
        raise BaseUserBadNameException from exception
    except PlaylistBadNameException as exception:
        base_users_service_logger.exception(f"Bad Playlist Parameter: {playlist_name}")
        raise PlaylistBadNameException from exception
    except UserUnauthorizedException as exception:
        base_users_service_logger.exception(
            f"Unathorized user {user_name} for adding saved playlists"
        )
        raise UserUnauthorizedException from exception
    except PlaylistNotFoundException as exception:
        base_users_service_logger.exception(f"Playlist not found: {playlist_name}")
        raise PlaylistNotFoundException from exception
    except BaseUserRepositoryException as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Repository adding playlist {playlist_name} "
            f"to user {user_name} saved playlist"
        )
        raise BaseUserServiceException from exception
    except Exception as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Service adding playlist {playlist_name} "
            f"to user {user_name} saved playlist"
        )
        raise BaseUserServiceException from exception
    else:
        base_users_service_logger.info(
            f"Playlist {playlist_name} added to User {user_name} saved playlists"
        )


def delete_saved_playlist(user_name: str, playlist_name: str, token: TokenData) -> None:
    """Deletes saved playlist from user

    Args:
        user_name (str): user name
        playlist_name (str): playlist name
        token (TokenData): token data from user

    Raises:
        BaseUserBadNameException: invalid user name
        PlaylistBadNameException: invalid playlist name
        UserUnauthorizedException: user cannot access a playlist that is created by him
        PlaylistNotFoundException: playlist doesn't exists
        BaseUserServiceException: unexpected error deleting saved playlist from user
    """
    try:
        base_user_service_validations.validate_user_name_parameter(user_name)
        playlist_service.validate_playlist_name_parameter(playlist_name)
        auth_service.validate_jwt_user_matches_user(token, user_name)
        base_user_service_validations.validate_user_should_exists(user_name)
        playlist_service.validate_playlist_should_exists(playlist_name)

        base_user_repository.delete_saved_playlist(
            user_name=user_name,
            playlist_name=playlist_name,
            collection=user_collection_provider.get_user_associated_collection(user_name),
        )
    except BaseUserBadNameException as exception:
        base_users_service_logger.exception(f"Bad User Parameter: {user_name}")
        raise BaseUserBadNameException from exception
    except PlaylistBadNameException as exception:
        base_users_service_logger.exception(f"Bad Playlist Parameter: {playlist_name}")
        raise PlaylistBadNameException from exception
    except UserUnauthorizedException as exception:
        base_users_service_logger.exception(
            f"Unathorized user {user_name} for deleting saved playlists"
        )
        raise UserUnauthorizedException from exception
    except PlaylistNotFoundException as exception:
        base_users_service_logger.exception(f"Playlist not found: {playlist_name}")
        raise PlaylistNotFoundException from exception
    except BaseUserRepositoryException as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Repository deleting playlist {playlist_name} "
            f"from user {user_name} saved playlist"
        )
        raise BaseUserServiceException from exception
    except Exception as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Service deleting playlist {playlist_name} "
            f"from user {user_name} saved playlist"
        )
        raise BaseUserServiceException from exception
    else:
        base_users_service_logger.info(
            f"Playlist {playlist_name} deleted from User {user_name} saved playlists"
        )


def add_playlist_to_owner(user_name: str, playlist_name: str, token: TokenData) -> None:
    """Add playlist to owner

    Args:
        user_name (str): user name
        playlist_name (str): playlist name
        token (TokenData): user token info

    Raises:
        BaseUserServiceException: unexpected error adding playlist to owner
    """
    try:
        base_user_service_validations.validate_user_name_parameter(user_name)
        validate_playlist_name_parameter(playlist_name)
        auth_service.validate_jwt_user_matches_user(token, user_name)
        base_user_service_validations.validate_user_should_exists(user_name)
        validate_playlist_should_exists(playlist_name)

        base_user_repository.add_playlist_to_owner(
            user_name=user_name,
            playlist_name=playlist_name,
            collection=user_collection_provider.get_user_associated_collection(user_name),
        )

        base_users_service_logger.info(
            f"Playlist {playlist_name} added to owner {user_name} created playlists"
        )
    except BaseUserRepositoryException as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Repository adding playlist {playlist_name} "
            f"to owner {user_name}"
        )
        raise BaseUserServiceException from exception
    except Exception as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Service adding playlist {playlist_name} "
            f"to owner {user_name}"
        )
        raise BaseUserServiceException from exception


def delete_playlist_from_owner(playlist_name: str) -> None:
    """Delete playlist from owner

    Args:
        playlist_name (str): playlist name

    Raises:
        BaseUserServiceException: unexpected error deleting playlist from owner
    """
    try:
        validate_playlist_name_parameter(playlist_name)
        validate_playlist_should_exists(playlist_name)

        user_name = playlist_service.get_playlist(playlist_name).owner

        base_user_service_validations.validate_user_should_exists(user_name)

        base_user_repository.delete_playlist_from_owner(
            user_name=user_name,
            playlist_name=playlist_name,
            collection=user_collection_provider.get_user_associated_collection(user_name),
        )

        base_users_service_logger.info(
            f"Playlist {playlist_name} deleted from owner {user_name} created playlists"
        )
    except BaseUserRepositoryException as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Repository deleting playlist {playlist_name} "
            f"from owner {user_name}"
        )
        raise BaseUserServiceException from exception
    except Exception as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Service deleting playlist {playlist_name} "
            f"from owner {user_name}"
        )
        raise BaseUserServiceException from exception


def update_playlist_name(old_playlist_name: str, new_playlist_name: str) -> None:
    """Update playlist name on users that have it saved, liked or it's the owner

    Args:
        old_playlist_name (str): old name
        new_playlist_name (str): new name
    """
    validate_playlist_name_parameter(old_playlist_name)
    validate_playlist_name_parameter(new_playlist_name)

    if old_playlist_name == new_playlist_name:
        return

    for collection in user_collection_provider.get_all_collections():
        base_user_repository.update_playlist_name(
            old_playlist_name=old_playlist_name,
            new_playlist_name=new_playlist_name,
            collection=collection,
        )


def get_user_relevant_playlists(user_name: str) -> list[PlaylistDTO]:
    """Get user relevant playlists

    Args:
        user_name (str): user name

    Raises:
        BaseUserBadNameException: invalid user name
        BaseUserNotFoundException: user not found
        BaseUserServiceException: unexpected error getting relevant playlists from user

    Returns:
        list[PlaylistDTO]: the relevant playlists
    """
    try:
        base_user_service_validations.validate_user_name_parameter(user_name)
        base_user_service_validations.validate_user_should_exists(user_name)
        collection = user_collection_provider.get_user_associated_collection(user_name)
        relevant_playlist_names = base_user_repository.get_user_relevant_playlist_names(
            user_name, collection
        )
        relevant_playlists = playlist_service.get_selected_playlists(relevant_playlist_names)
    except BaseUserBadNameException as exception:
        base_users_service_logger.exception(f"Bad user Parameter: {user_name}")
        raise BaseUserBadNameException from exception
    except BaseUserNotFoundException as exception:
        base_users_service_logger.exception(f"User not found: {user_name}")
        raise BaseUserNotFoundException from exception
    except BaseUserRepositoryException as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Repository getting user relevant playlists "
            f"from user {user_name}"
        )
        raise BaseUserServiceException from exception
    except PlaylistServiceException as exception:
        base_users_service_logger.exception(
            f"Unexpected error in Playlist Service getting user relevant playlists "
            f"from user {user_name}"
        )
        raise BaseUserServiceException from exception
    except Exception as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Service getting user relevant playlists "
            f"from user {user_name}"
        )
        raise BaseUserServiceException from exception
    else:
        return relevant_playlists


def get_user_playlists(user_name: str) -> list[PlaylistDTO]:
    """Get user created playlists

    Args:
        user_name (str): user name

    Raises:
        BaseUserBadNameException: invalid user name
        BaseUserNotFoundException: user not found
        BaseUserServiceException: unexpected error getting playlists created by the user

    Returns:
        list[PlaylistDTO]: the playlists created by the user
    """
    try:
        base_user_service_validations.validate_user_name_parameter(user_name)
        base_user_service_validations.validate_user_should_exists(user_name)
        collection = user_collection_provider.get_user_associated_collection(user_name)
        user_playlist_names = base_user_repository.get_user_playlist_names(
            user_name, collection
        )
        user_playlists = playlist_service.get_selected_playlists(user_playlist_names)
    except BaseUserBadNameException as exception:
        base_users_service_logger.exception(f"Bad user Parameter: {user_name}")
        raise BaseUserBadNameException from exception
    except BaseUserNotFoundException as exception:
        base_users_service_logger.exception(f"User not found: {user_name}")
        raise BaseUserNotFoundException from exception
    except BaseUserRepositoryException as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Repository getting playlists created "
            f"by user {user_name}"
        )
        raise BaseUserServiceException from exception
    except PlaylistServiceException as exception:
        base_users_service_logger.exception(
            f"Unexpected error in Playlist Service getting playlists created "
            f"by user {user_name}"
        )
        raise BaseUserServiceException from exception
    except Exception as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Service getting playlists created "
            f"by user {user_name}"
        )
        raise BaseUserServiceException from exception
    else:
        return user_playlists


def get_user_playlist_names(user_name: str) -> list[str]:
    """Get user created playlist names

    Args:
        user_name (str): user name

    Raises:
        BaseUserBadNameException: invalid user name
        BaseUserNotFoundException: user not found
        BaseUserServiceException: unexpected error getting playlist names from user

    Returns:
        list[str]: the playlist names created by the user
    """
    try:
        base_user_service_validations.validate_user_name_parameter(user_name)
        base_user_service_validations.validate_user_should_exists(user_name)
        collection = user_collection_provider.get_user_associated_collection(user_name)
        user_playlist_names = base_user_repository.get_user_playlist_names(
            user_name, collection
        )
    except BaseUserBadNameException as exception:
        base_users_service_logger.exception(f"Bad user Parameter: {user_name}")
        raise BaseUserBadNameException from exception
    except BaseUserNotFoundException as exception:
        base_users_service_logger.exception(f"User not found: {user_name}")
        raise BaseUserNotFoundException from exception
    except BaseUserRepositoryException as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Repository getting user playlist names "
            f"from owner {user_name}"
        )
        raise BaseUserServiceException from exception
    except Exception as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Service getting user playlist names "
            f"from owner {user_name}"
        )
        raise BaseUserServiceException from exception
    else:
        return user_playlist_names


def get_user_playback_history(user_name: str) -> list[SongMetadataDTO]:
    """Get user song playback history

    Args:
        user_name (str): user name

    Raises:
        BaseUserBadNameException: invalid user name
        BaseUserNotFoundException: user not found
        BaseUserServiceException: unexpected error getting playback history from user

    Returns:
        list[str]: the song playback history from user
    """
    try:
        base_user_service_validations.validate_user_name_parameter(user_name)
        base_user_service_validations.validate_user_should_exists(user_name)
        collection = user_collection_provider.get_user_associated_collection(user_name)
        playback_history_names = base_user_repository.get_user_playback_history_names(
            user_name=user_name, collection=collection
        )
        songs_metadata = base_song_service.get_songs_metadata(playback_history_names)

    except BaseUserBadNameException as exception:
        base_users_service_logger.exception(f"Bad user Parameter: {user_name}")
        raise BaseUserBadNameException from exception
    except BaseUserNotFoundException as exception:
        base_users_service_logger.exception(f"User not found: {user_name}")
        raise BaseUserNotFoundException from exception
    except BaseUserRepositoryException as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Repository getting playback history "
            f"from owner {user_name}"
        )
        raise BaseUserServiceException from exception
    except Exception as exception:
        base_users_service_logger.exception(
            f"Unexpected error in User Service getting getting playback history "
            f"from owner {user_name}"
        )
        raise BaseUserServiceException from exception
    else:
        return songs_metadata
