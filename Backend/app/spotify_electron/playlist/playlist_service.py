"""Playlist service for handling business logic"""

import app.spotify_electron.playlist.playlist_repository as playlist_repository
import app.spotify_electron.song.validations.base_song_service_validations as base_song_service_validations  # noqa: E501
import app.spotify_electron.user.base_user_service as base_user_service
import app.spotify_electron.user.validations.base_user_service_validations as base_user_service_validations  # noqa: E501
from app.auth.auth_schema import (
    TokenData,
    UserUnauthorizedError,
)
from app.auth.auth_service_validations import validate_jwt_user_matches_user
from app.logging.logging_constants import LOGGING_PLAYLIST_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.playlist.playlist_schema import (
    PlaylistAlreadyExistsError,
    PlaylistBadNameError,
    PlaylistDTO,
    PlaylistNotFoundError,
    PlaylistRepositoryError,
    PlaylistServiceError,
    get_playlist_dto_from_dao,
)
from app.spotify_electron.playlist.validations.playlist_service_validations import (
    validate_playlist_name_parameter,
    validate_playlist_should_exists,
    validate_playlist_should_not_exists,
)
from app.spotify_electron.song.base_song_schema import (
    SongBadNameError,
    SongNotFoundError,
    SongRepositoryError,
)
from app.spotify_electron.user.user.user_schema import UserNotFoundError
from app.spotify_electron.utils.date.date_utils import get_current_iso8601_date
from typing import Any

playlist_service_logger = SpotifyElectronLogger(LOGGING_PLAYLIST_SERVICE).get_logger()


async def check_playlist_exists(name: str) -> bool:
    """Returns if playlist exists

    Args:
    ----
        name: playlist name

    Returns:
    -------
        if the playlist exists
    """
    return await playlist_repository.check_playlist_exists(name)


async def get_playlist(name: str) -> PlaylistDTO:
    """Returns the playlist

    Args:
    ----
        name: name of the playlist

    Raises:
    ------
        PlaylistBadNameError: invalid playlist name
        PlaylistNotFoundError: playlist not found
        PlaylistServiceError: unexpected error while getting playlist

    Returns:
    -------
        the playlist
    """
    try:
        validate_playlist_name_parameter(name)
        playlist = await playlist_repository.get_playlist(name)
        playlist_dto = get_playlist_dto_from_dao(playlist)
    except PlaylistBadNameError as exception:
        playlist_service_logger.exception(f"Bad Playlist Name Parameter: {name}")
        raise PlaylistBadNameError from exception
    except PlaylistNotFoundError as exception:
        playlist_service_logger.exception(f"Playlist not found: {name}")
        raise PlaylistNotFoundError from exception
    except PlaylistRepositoryError as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository getting playlist: {name}"
        )
        raise PlaylistServiceError from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service getting playlist: {name}"
        )
        raise PlaylistServiceError from exception
    else:
        playlist_service_logger.info(f"Playlist {name} retrieved successfully")
        return playlist_dto


async def create_playlist(
    name: str, photo: str, description: str, song_names: list[str], token: TokenData
) -> None:
    """Creates a playlist

    Args:
    ----
        name: name
        photo: thumbnail photo
        description: description
        song_names: list of song names
        token: token user info

    Raises:
    ------
        PlaylistBadNameError: invalid playlist name
        PlaylistAlreadyExistsError: playlist already exists
        UserNotFoundError: user doesn't exists
        PlaylistServiceError: unexpected error while creating playlist
    """
    try:
        owner = token.username

        date = get_current_iso8601_date()

        validate_playlist_name_parameter(name)
        await validate_playlist_should_not_exists(name)
        await base_user_service_validations.validate_user_should_exists(owner)

        await playlist_repository.create_playlist(
            name,
            photo if "http" in photo else "",
            date,
            description,
            owner,
            song_names,
        )
        await base_user_service.add_playlist_to_owner(
            user_name=owner, playlist_name=name, token=token
        )
    except PlaylistBadNameError as exception:
        playlist_service_logger.exception(f"Bad Playlist Name Parameter: {name}")
        raise PlaylistBadNameError from exception
    except PlaylistAlreadyExistsError as exception:
        playlist_service_logger.exception(f"Playlist already exists: {name}")
        raise PlaylistAlreadyExistsError from exception
    except UserNotFoundError as exception:
        playlist_service_logger.exception(f"User not found: {name}")
        raise UserNotFoundError from exception
    except PlaylistRepositoryError as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository creating user: {name}"
        )
        raise PlaylistServiceError from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service creating user: {name}"
        )
        raise PlaylistServiceError from exception
    else:
        playlist_service_logger.info(f"Playlist {name} created successfully")


async def update_playlist(  # noqa: PLR0917
    name: str,
    new_name: str | None,
    photo: str,
    description: str,
    song_names: list[str],
    token: TokenData,
) -> None:
    """Updates a playlist

    Args:
    ----
        name: name
        new_name: new playlist name, optional
        photo: thumbnail photo
        description: description
        song_names: list of song names
        token: token user info

    Raises:
    ------
        PlaylistBadNameError: invalid playlist name
        PlaylistNotFoundError: playlist doesn't exists
        UserUnauthorizedError: user is not the owner of playlist
        PlaylistServiceError: unexpected error while updating playlist
    """
    try:
        validate_playlist_name_parameter(name)
        await validate_playlist_should_exists(name)

        playlist = await playlist_repository.get_playlist(name)

        validate_jwt_user_matches_user(token, playlist.owner)

        if not new_name:
            await playlist_repository.update_playlist(
                name, name, photo if "http" in photo else "", description, song_names
            )
            return

        validate_playlist_name_parameter(new_name)
        await playlist_repository.update_playlist(
            name,
            new_name,
            photo if "http" in photo else "",
            description,
            song_names,
        )

        await base_user_service.update_playlist_name(name, new_name)
    except PlaylistBadNameError as exception:
        playlist_service_logger.exception(f"Bad Playlist Name Parameter: {name}")
        raise PlaylistBadNameError from exception
    except PlaylistNotFoundError as exception:
        playlist_service_logger.exception(f"Playlist not found: {name}")
        raise PlaylistNotFoundError from exception
    except UserUnauthorizedError as exception:
        playlist_service_logger.exception(f"User is not the owner of playlist: {name}")
        raise UserUnauthorizedError from exception
    except PlaylistRepositoryError as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository updating playlist: {name}"
        )
        raise PlaylistServiceError from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service updating playlist: {name}"
        )
        raise PlaylistServiceError from exception
    else:
        playlist_service_logger.info(f"Playlist {name} updated successfully")


async def update_playlist_metadata(
    name: str,
    token: TokenData,
    new_name: str | None = None,
    description: str | None = None,
    photo: str | None = None,
    is_collaborative: bool | None = None,
    is_public: bool | None = None,
) -> None:
    """Update playlist metadata.

    Args:
        name: The current name of the playlist
        token: The user's authentication token
        new_name: Optional new name for the playlist
        description: Optional new description
        photo: Optional new photo URL
        is_collaborative: Optional new collaborative status
        is_public: Optional new public status

    Raises:
        PlaylistBadNameError: If the name is invalid
        PlaylistNotFoundError: If the playlist doesn't exist
        UserUnauthorizedError: If the user is not the owner
        PlaylistServiceError: For unexpected errors
    """
    try:
        validate_playlist_name_parameter(name)
        await validate_playlist_should_exists(name)
        playlist = await playlist_repository.get_playlist(name)
        validate_jwt_user_matches_user(token, playlist.owner)
        
        update_fields: dict[str, Any] = {}
        
        if new_name:
            validate_playlist_name_parameter(new_name)
            update_fields["name"] = new_name
        if description is not None:
            update_fields["description"] = description
        if photo is not None:
            update_fields["photo"] = photo if "http" in photo else ""
        if is_collaborative is not None:
            update_fields["is_collaborative"] = is_collaborative
        if is_public is not None:
            update_fields["is_public"] = is_public
            
        if not update_fields:
            return  # Nothing to update
            
        await playlist_repository.update_playlist_metadata(name, update_fields)
        if new_name:
            await base_user_service.update_playlist_name(name, new_name)
            
    except PlaylistBadNameError as exception:
        playlist_service_logger.exception(f"Bad Playlist Name Parameter: {name}")
        raise PlaylistBadNameError from exception
    except PlaylistNotFoundError as exception:
        playlist_service_logger.exception(f"Playlist not found: {name}")
        raise PlaylistNotFoundError from exception
    except UserUnauthorizedError as exception:
        playlist_service_logger.exception(f"User is not the owner of playlist: {name}")
        raise UserUnauthorizedError from exception
    except PlaylistRepositoryError as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository updating playlist metadata: {name}"
        )
        raise PlaylistServiceError from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service updating playlist metadata: {name}"
        )
        raise PlaylistServiceError from exception
    else:
        playlist_service_logger.info(f"Playlist {name} metadata updated successfully")


async def delete_playlist(name: str) -> None:
    """Delete a playlist

    Args:
    ----
        name: playlist name

    Raises:
    ------
        PlaylistBadNameError: invalid playlist name
        PlaylistNotFoundError: playlist doesn't exists
        UserNotFoundError: user doesn't exists
        PlaylistServiceError: unexpected error while deleting playlist
    """
    try:
        validate_playlist_name_parameter(name)
        await validate_playlist_should_exists(name)
        await base_user_service.delete_playlist_from_owner(playlist_name=name)
        await playlist_repository.delete_playlist(name)
    except PlaylistBadNameError as exception:
        playlist_service_logger.exception(f"Bad Playlist Name Parameter: {name}")
        raise PlaylistBadNameError from exception
    except PlaylistNotFoundError as exception:
        playlist_service_logger.exception(f"Playlist not found: {name}")
        raise PlaylistNotFoundError from exception
    except UserNotFoundError as exception:
        playlist_service_logger.exception(f"User owner of the playlist {name} not found")
        raise UserNotFoundError from exception
    except PlaylistRepositoryError as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository deleting playlist:{name}"
        )
        raise PlaylistServiceError from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service deleting playlist:{name}"
        )
        raise PlaylistServiceError from exception
    else:
        playlist_service_logger.info(f"Playlist {name} deleted successfully")


async def get_all_playlist() -> list[PlaylistDTO]:
    """Gets all playlists

    Raises
    ------
        PlaylistServiceError: unexpected error while getting all playlists

    Returns
    -------
        the list of playlists
    """
    try:
        playlists = await playlist_repository.get_all_playlists()
        playlists_dto = [get_playlist_dto_from_dao(playlist) for playlist in playlists]
    except PlaylistRepositoryError as exception:
        playlist_service_logger.exception(
            "Unexpected error in Playlist Repository getting all playlists"
        )
        raise PlaylistServiceError from exception
    except Exception as exception:
        playlist_service_logger.exception(
            "Unexpected error in Playlist Service getting all playlists"
        )
        raise PlaylistServiceError from exception
    else:
        playlist_service_logger.info("All Playlists retrieved successfully")
        return playlists_dto


async def get_selected_playlists(playlist_names: list[str]) -> list[PlaylistDTO]:
    """Get selected playlist

    Args:
    ----
        playlist_names: list with playlists names

    Raises:
    ------
        PlaylistServiceError: unexpected error while getting selected playlist

    Returns:
    -------
        the list of selected playlists
    """
    try:
        playlists = await playlist_repository.get_selected_playlists(playlist_names)
        playlists_dto = [get_playlist_dto_from_dao(playlist) for playlist in playlists]
    except PlaylistRepositoryError as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository getting selected playlists: "
            f"{playlist_names}"
        )
        raise PlaylistServiceError from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service getting selected playlists: "
            f"{playlist_names}"
        )
        raise PlaylistServiceError from exception
    else:
        playlist_service_logger.info(
            f"Selected Playlists {playlist_names} retrieved successfully"
        )
        return playlists_dto


async def search_by_name(name: str) -> list[PlaylistDTO]:
    """Gets playlists with partially matching name

    Args:
    ----
        name: name to match

    Raises:
    ------
        PlaylistServiceError: unexpected error while getting playlist that matches a name

    Returns:
    -------
        a list with playlists that matches the name
    """
    try:
        playlists = await playlist_repository.get_playlist_search_by_name(name)
        playlists_dto = [get_playlist_dto_from_dao(playlist) for playlist in playlists]
    except PlaylistRepositoryError as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository searching playlist by name {name}"
        )
        raise PlaylistServiceError from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service searching playlist by name {name}"
        )
        raise PlaylistServiceError from exception
    else:
        playlist_service_logger.info(
            f"Playlists searched by name {name} retrieved successfully"
        )
        return playlists_dto


async def add_songs_to_playlist(playlist_name: str, song_names: list[str]) -> None:
    """Add songs to playlist

    Args:
        playlist_name: playlist name
        song_names: song names

    Raises:
        PlaylistBadNameError: name
        PlaylistNotFoundError: playlist doesn't exists
        SongBadNameError: invalid song name
        SongNotFoundError: song not found
        PlaylistServiceError: unexpected error adding songs to playlist
    """
    try:
        validate_playlist_name_parameter(playlist_name)
        await validate_playlist_should_exists(playlist_name)
        for name in song_names:
            base_song_service_validations.validate_song_name_parameter(name)
            await base_song_service_validations.validate_song_should_exists(name)
        await playlist_repository.add_songs_to_playlist(playlist_name, song_names)
    except PlaylistBadNameError as exception:
        playlist_service_logger.exception(f"Bad Playlist Name Parameter: {playlist_name}")
        raise PlaylistBadNameError from exception
    except PlaylistNotFoundError as exception:
        playlist_service_logger.exception(f"Playlist not found: {playlist_name}")
        raise PlaylistNotFoundError from exception
    except SongBadNameError as exception:
        playlist_service_logger.exception(f"Not all the songs have valid names: {song_names}")
        raise SongBadNameError from exception
    except SongNotFoundError as exception:
        playlist_service_logger.exception(f"Not all the songs were found: {song_names}")
        raise SongNotFoundError from exception
    except PlaylistRepositoryError as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository "
            f"adding songs to playlist {playlist_name}: {song_names}"
        )
        raise PlaylistServiceError from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service "
            f"adding songs to playlist {playlist_name}: {song_names}"
        )
        raise PlaylistServiceError from exception
    else:
        playlist_service_logger.info(f"Songs added to playlist {playlist_name}: {song_names}")


async def remove_songs_from_playlist(playlist_name: str, song_names: list[str]) -> None:
    """Remove songs from playlist

    Args:
        playlist_name: playlist name
        song_names: song names

    Raises:
        PlaylistBadNameError: name
        PlaylistNotFoundError: playlist doesn't exists
        SongBadNameError: invalid song name
        SongNotFoundError: song not found
        PlaylistServiceError: unexpected error removing songs from playlist
    """
    try:
        validate_playlist_name_parameter(playlist_name)
        await validate_playlist_should_exists(playlist_name)
        for name in song_names:
            base_song_service_validations.validate_song_name_parameter(name)
            await base_song_service_validations.validate_song_should_exists(name)
        await playlist_repository.remove_songs_from_playlist(playlist_name, song_names)
    except PlaylistBadNameError as exception:
        playlist_service_logger.exception(f"Bad Playlist Name Parameter: {playlist_name}")
        raise PlaylistBadNameError from exception
    except PlaylistNotFoundError as exception:
        playlist_service_logger.exception(f"Playlist not found: {playlist_name}")
        raise PlaylistNotFoundError from exception
    except SongBadNameError as exception:
        playlist_service_logger.exception(f"Not all the songs have valid names: {song_names}")
        raise SongBadNameError from exception
    except SongNotFoundError as exception:
        playlist_service_logger.exception(f"Not all the songs were found: {song_names}")
        raise SongNotFoundError from exception
    except SongRepositoryError as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Song Repository checking if songs exist: {song_names}"
        )
        raise PlaylistServiceError from exception
    except PlaylistRepositoryError as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Repository "
            f"removing songs from playlist {playlist_name}: {song_names}"
        )
        raise PlaylistServiceError from exception
    except Exception as exception:
        playlist_service_logger.exception(
            f"Unexpected error in Playlist Service "
            f"removing songs from playlist {playlist_name}: {song_names}"
        )
        raise PlaylistServiceError from exception
    else:
        playlist_service_logger.info(
            f"Songs removed from playlist {playlist_name}: {song_names}"
        )
