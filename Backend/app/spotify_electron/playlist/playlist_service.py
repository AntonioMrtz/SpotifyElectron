"""
Playlist service for handling business logic
"""

import app.auth.auth_service as auth_service
import app.spotify_electron.playlist.playlist_repository as playlist_repository
import app.spotify_electron.song.validations.base_song_service_validations as base_song_service_validations  # noqa: E501
import app.spotify_electron.user.base_user_service as base_user_service
import app.spotify_electron.user.validations.base_user_service_validations as base_user_service_validations  # noqa: E501
from app.auth.auth_schema import (
    TokenData,
    UserUnauthorizedException,
)
from app.logging.logging_constants import LOGGING_PLAYLIST_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.playlist.playlist_schema import (
    PlaylistAlreadyExistsException,
    PlaylistBadNameException,
    PlaylistDTO,
    PlaylistNotFoundException,
    PlaylistRepositoryException,
    PlaylistServiceException,
    get_playlist_dto_from_dao,
)
from app.spotify_electron.playlist.validations.playlist_service_validations import (
    validate_playlist_name_parameter,
    validate_playlist_should_exists,
    validate_playlist_should_not_exists,
)
from app.spotify_electron.song.base_song_schema import (
    SongBadNameException,
    SongNotFoundException,
    SongRepositoryException,
)
from app.spotify_electron.user.user.user_schema import UserNotFoundException
from app.spotify_electron.utils.date.date_utils import get_current_iso8601_date

playlist_service_logger = SpotifyElectronLogger(LOGGING_PLAYLIST_SERVICE).getLogger()


def check_playlist_exists(name: str) -> bool:
    """Returns if playlist exists

    Args:
    ----
        name (str): playlist name

    Returns:
    -------
        bool: if the playlist exists

    """
    return playlist_repository.check_playlist_exists(name)


def get_playlist(name: str) -> PlaylistDTO:
    """Returns the playlist

    Args:
    ----
        name (str): name of the playlist

    Raises:
    ------
        PlaylistBadNameException: invalid playlist name
        PlaylistNotFoundException: playlist not found
        PlaylistServiceException: unexpected error while getting playlist

    Returns:
    -------
        PlaylistDTO: the playlist

    """
    try:
        validate_playlist_name_parameter(name)
        playlist = playlist_repository.get_playlist(name)
        playlist_dto = get_playlist_dto_from_dao(playlist)
    except PlaylistBadNameException as exception:
        playlist_service_logger.exception(f"Bad Playlist Name Parameter: {name}")
        raise PlaylistBadNameException from exception
    except PlaylistNotFoundException as exception:
        playlist_service_logger.exception(f"Playlist not found: {name}")
        raise PlaylistNotFoundException from exception
    except PlaylistRepositoryException as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository getting playlist: {name}"
        )
        raise PlaylistServiceException from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service getting playlist: {name}"
        )
        raise PlaylistServiceException from exception
    else:
        playlist_service_logger.info(f"Playlist {name} retrieved successfully")
        return playlist_dto


def create_playlist(
    name: str, photo: str, description: str, song_names: list[str], token: TokenData
) -> None:
    """Creates a playlist

    Args:
    ----
        name (str): name
        photo (str): thumbnail photo
        description (str): description
        song_names (list): list of song names
        token (TokenData): token user info

    Raises:
    ------
        PlaylistBadNameException: invalid playlist name
        PlaylistAlreadyExistsException: playlist already exists
        UserNotFoundException: user doesn't exists
        PlaylistServiceException: unexpected error while creating playlist

    """
    try:
        owner = token.username

        date = get_current_iso8601_date()

        validate_playlist_name_parameter(name)
        validate_playlist_should_not_exists(name)
        base_user_service_validations.validate_user_should_exists(owner)

        playlist_repository.create_playlist(
            name,
            photo if "http" in photo else "",
            date,
            description,
            owner,
            song_names,
        )
        base_user_service.add_playlist_to_owner(
            user_name=owner, playlist_name=name, token=token
        )
    except PlaylistBadNameException as exception:
        playlist_service_logger.exception(f"Bad Playlist Name Parameter: {name}")
        raise PlaylistBadNameException from exception
    except PlaylistAlreadyExistsException as exception:
        playlist_service_logger.exception(f"Playlist already exists: {name}")
        raise PlaylistAlreadyExistsException from exception
    except UserNotFoundException as exception:
        playlist_service_logger.exception(f"User not found: {name}")
        raise UserNotFoundException from exception
    except PlaylistRepositoryException as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository creating user: {name}"
        )
        raise PlaylistServiceException from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service creating user: {name}"
        )
        raise PlaylistServiceException from exception
    else:
        playlist_service_logger.info(f"Playlist {name} created successfully")


def update_playlist_metadata(
    token: TokenData,
    name: str,
    new_name: str | None = None,
    photo: str | None = None,
    description: str | None = None,
) -> None:
    """
    Updates only specified fields of a playlist's metadata.

    Args:
        token (TokenData): The token containing user information.
        name (str): The current name of the playlist to identify it.
        new_name (str | None): The new name of the playlist, if updating the name.
        photo (str | None): The new thumbnail photo URL for the playlist, if provided.
        description (str | None): The new description for the playlist, if provided.

    Raises:
        PlaylistBadNameException: Raised if the playlist name (current or new) is invalid.
        PlaylistNotFoundException: Raised if the playlist does not exist.
        UserUnauthorizedException: Raised if the user is not the owner of the playlist.
        PlaylistServiceException: Raised for unexpected errors during the update.
    """
    try:
        validate_and_get_playlist(name, token)
        update_data = collect_update_data(new_name, photo, description)
        perform_update(name, update_data)
    except PlaylistBadNameException:
        playlist_service_logger.exception(
            f"Invalid playlist name parameter for playlist: {name}"
        )
        raise
    except PlaylistNotFoundException:
        playlist_service_logger.exception(f"Playlist not found: {name}")
        raise
    except UserUnauthorizedException:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service updating playlist: {name}"
        )
        raise
    except PlaylistRepositoryException as e:
        playlist_service_logger.exception(
            f"Repository error while updating playlist: {name}"
        )
        raise PlaylistServiceException from e
    except Exception as e:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service while updating playlist: {name}"
        )
        raise PlaylistServiceException from e
    else:
        playlist_service_logger.info(
            f"Playlist {name} updated successfully with fields: {update_data}"
        )


def validate_and_get_playlist(name: str, token: TokenData) -> None:
    """
    Validates the playlist name, checks existence, retrieves the playlist,
    and verifies user authorization.

    Args:
        name (str): The name of the playlist.
        token (TokenData): The token containing user information.

    Raises:
        PlaylistBadNameException: If the playlist name is invalid.
        PlaylistNotFoundException: If the playlist does not exist.
        UserUnauthorizedException: If the user is not authorized to update the playlist.
    """
    validate_playlist_name_parameter(name)
    validate_playlist_should_exists(name)
    playlist_repository.get_playlist(name)
    auth_service.validate_jwt_user_matches_user(
        token, playlist_repository.get_playlist(name).owner
    )


def collect_update_data(
        new_name: str | None,
        photo: str | None,
        description: str | None) -> dict:
    """
    Collects and validates the update data based on provided parameters.

    Args:
        new_name (str | None): The new name of the playlist.
        photo (str | None): The new photo URL for the playlist.
        description (str | None): The new description for the playlist.

    Returns:
        dict: A dictionary containing the fields to be updated.
    """
    update_data = {}
    if new_name:
        validate_playlist_name_parameter(new_name)
        update_data["new_name"] = new_name
    if photo and "http" in photo:
        update_data["photo"] = photo
    if description:
        update_data["description"] = description
    return update_data


def perform_update(name: str, update_data: dict) -> None:
    """
    Performs the update operation on the playlist repository and updates
    the playlist name in the user service if a new name is provided.

    Args:
        name (str): The current name of the playlist.
        update_data (dict): The data to update in the playlist.
    """
    if update_data:
        playlist_repository.update_playlist_metadata(name, **update_data)
        if "new_name" in update_data:
            base_user_service.update_playlist_name(name, update_data["new_name"])


def delete_playlist(name: str) -> None:
    """Delete a playlist

    Args:
    ----
        name (str): playlist name

    Raises:
    ------
        PlaylistBadNameException: invalid playlist name
        PlaylistNotFoundException: playlist doesn't exists
        PlaylistServiceException: unexpected error while deleting playlist

    """
    try:
        validate_playlist_name_parameter(name)
        validate_playlist_should_exists(name)
        base_user_service.delete_playlist_from_owner(playlist_name=name)
        playlist_repository.delete_playlist(name)
    except PlaylistBadNameException as exception:
        playlist_service_logger.exception(f"Bad Playlist Name Parameter: {name}")
        raise PlaylistBadNameException from exception
    except PlaylistNotFoundException as exception:
        playlist_service_logger.exception(f"Playlist not found: {name}")
        raise PlaylistNotFoundException from exception
    except UserNotFoundException as exception:
        playlist_service_logger.exception(f"User owner of the playlist {name} not found")
        raise UserNotFoundException from exception
    except PlaylistRepositoryException as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository deleting playlist:{name}"
        )
        raise PlaylistServiceException from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service deleting playlist:{name}"
        )
        raise PlaylistServiceException from exception
    else:
        playlist_service_logger.info(f"Playlist {name} deleted successfully")


def get_all_playlist() -> list[PlaylistDTO]:
    """Gets all playlists

    Raises
    ------
        PlaylistServiceException: unexpected error while getting all playlists

    Returns
    -------
        list[PlaylistDTO]: the list of playlists

    """
    try:
        playlists = playlist_repository.get_all_playlists()
        playlists_dto = [get_playlist_dto_from_dao(playlist) for playlist in playlists]
    except PlaylistRepositoryException as exception:
        playlist_service_logger.exception(
            "Unexpected error in Playlist Repository getting all playlists"
        )
        raise PlaylistServiceException from exception
    except Exception as exception:
        playlist_service_logger.exception(
            "Unexpected error in Playlist Service getting all playlists"
        )
        raise PlaylistServiceException from exception
    else:
        playlist_service_logger.info("All Playlists retrieved successfully")
        return playlists_dto


def get_selected_playlists(playlist_names: list[str]) -> list[PlaylistDTO]:
    """Get selected playlist

    Args:
    ----
        playlist_names (list[str]): list with playlists names

    Raises:
    ------
        PlaylistServiceException: unexpected error while getting selected playlist

    Returns:
    -------
        list[PlaylistDTO]: the list of selected playlists

    """
    try:
        playlists = playlist_repository.get_selected_playlists(playlist_names)
        playlists_dto = [get_playlist_dto_from_dao(playlist) for playlist in playlists]
    except PlaylistRepositoryException as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository getting selected playlists: "
            f"{playlist_names}"
        )
        raise PlaylistServiceException from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service getting selected playlists: "
            f"{playlist_names}"
        )
        raise PlaylistServiceException from exception
    else:
        playlist_service_logger.info(
            f"Selected Playlists {playlist_names} retrieved successfully"
        )
        return playlists_dto


def search_by_name(name: str) -> list[PlaylistDTO]:
    """Gets playlists with partially matching name

    Args:
    ----
        name (str): name to match

    Raises:
    ------
        PlaylistServiceException: unexpected error while getting playlist that matches a name

    Returns:
    -------
        list[PlaylistDTO]: a list with playlists that matches the name

    """
    try:
        playlists = playlist_repository.get_playlist_search_by_name(name)
        playlists_dto = [get_playlist_dto_from_dao(playlist) for playlist in playlists]
    except PlaylistRepositoryException as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository searching playlist by name {name}"
        )
        raise PlaylistServiceException from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service searching playlist by name {name}"
        )
        raise PlaylistServiceException from exception
    else:
        playlist_service_logger.info(
            f"Playlists searched by name {name} retrieved successfully"
        )
        return playlists_dto


def add_songs_to_playlist(playlist_name: str, song_names: list[str]) -> None:
    """Add songs to playlist

    Args:
        playlist_name (str): playlist name
        song_names (list[str]): song names

    Raises:
        PlaylistBadNameException: invalid playlist name
        PlaylistNotFoundException: playlist doesn't exists
        SongBadNameException: invalid song name
        SongNotFoundException: song not found
        PlaylistServiceException: unexpected error adding songs to playlist
    """
    try:
        validate_playlist_name_parameter(playlist_name)
        validate_playlist_should_exists(playlist_name)
        for name in song_names:
            base_song_service_validations.validate_song_name_parameter(name)
            base_song_service_validations.validate_song_should_exists(name)
        playlist_repository.add_songs_to_playlist(playlist_name, song_names)
    except PlaylistBadNameException as exception:
        playlist_service_logger.exception(f"Bad Playlist Name Parameter: {playlist_name}")
        raise PlaylistBadNameException from exception
    except PlaylistNotFoundException as exception:
        playlist_service_logger.exception(f"Playlist not found: {playlist_name}")
        raise PlaylistNotFoundException from exception
    except SongBadNameException as exception:
        playlist_service_logger.exception(f"Not all the songs have valid names: {song_names}")
        raise SongBadNameException from exception
    except SongNotFoundException as exception:
        playlist_service_logger.exception(f"Not all the songs were found: {song_names}")
        raise SongNotFoundException from exception
    except PlaylistRepositoryException as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository "
            f"adding songs to playlist {playlist_name}: {song_names}"
        )
        raise PlaylistServiceException from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service "
            f"adding songs to playlist {playlist_name}: {song_names}"
        )
        raise PlaylistServiceException from exception
    else:
        playlist_service_logger.info(f"Songs added to playlist {playlist_name}: {song_names}")


def remove_songs_from_playlist(playlist_name: str, song_names: list[str]) -> None:
    """Remove songs from playlist

    Args:
        playlist_name (str): playlist name
        song_names (list[str]): song names

    Raises:
        PlaylistBadNameException: invalid playlist name
        PlaylistNotFoundException: playlist doesn't exists
        SongBadNameException: invalid song name
        SongNotFoundException: song not found
        PlaylistServiceException: unexpected error removing songs from playlist
    """
    try:
        validate_playlist_name_parameter(playlist_name)
        validate_playlist_should_exists(playlist_name)
        for name in song_names:
            base_song_service_validations.validate_song_name_parameter(name)
            base_song_service_validations.validate_song_should_exists(name)
        playlist_repository.remove_songs_from_playlist(playlist_name, song_names)
    except PlaylistBadNameException as exception:
        playlist_service_logger.exception(f"Bad Playlist Name Parameter: {playlist_name}")
        raise PlaylistBadNameException from exception
    except PlaylistNotFoundException as exception:
        playlist_service_logger.exception(f"Playlist not found: {playlist_name}")
        raise PlaylistNotFoundException from exception
    except SongBadNameException as exception:
        playlist_service_logger.exception(f"Not all the songs have valid names: {song_names}")
        raise SongBadNameException from exception
    except SongNotFoundException as exception:
        playlist_service_logger.exception(f"Not all the songs were found: {song_names}")
        raise SongNotFoundException from exception
    except SongRepositoryException as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Song Repository checking if songs exist: {song_names}"
        )
        raise PlaylistServiceException from exception
    except PlaylistRepositoryException as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository "
            f"removing songs from playlist {playlist_name}: {song_names}"
        )
        raise PlaylistServiceException from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service "
            f"removing songs from playlist {playlist_name}: {song_names}"
        )
        raise PlaylistServiceException from exception
    else:
        playlist_service_logger.info(
            f"Songs removed from playlist {playlist_name}: {song_names}"
        )
