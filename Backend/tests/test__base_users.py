# TODO, only use user, move user tests here. Move artist tests into its own file
from pytest import fixture, mark
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

import app.auth.auth_service as auth_service
from app.spotify_electron.user.artist.artist_repository import (
    create_artist as create_artist_repo,
)
from app.spotify_electron.user.base_user_schema import (
    BaseUserDAO,
    BaseUserDocument,
    BaseUserDTO,
    get_base_user_dao_from_document,
    get_base_user_dto_from_dao,
)
from app.spotify_electron.user.base_user_service import (
    MAX_NUMBER_PLAYBACK_HISTORY_SONGS,
)
from app.spotify_electron.user.user.user_schema import UserType
from app.spotify_electron.utils.date.date_utils import get_current_iso8601_date
from tests.test_API.api_base_users import (
    delete_playlist_saved,
    get_user_playback_history,
    get_user_playlist_names,
    get_user_playlists,
    get_user_relevant_playlists,
    patch_history_playback,
    patch_playlist_saved,
    promote_user_to_artist,
    whoami,
)
from tests.test_API.api_login import post_login
from tests.test_API.api_test_artist import create_artist, get_artist
from tests.test_API.api_test_playlist import create_playlist, delete_playlist
from tests.test_API.api_test_song import create_song, delete_song
from tests.test_API.api_test_user import create_user, delete_user, get_user
from tests.test_API.api_token import get_user_jwt_header


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


def test_patch_playback_history_user_correct(clear_test_data_db):
    name = "8232392323623823723"
    password = "hola"
    artista = "artista"
    photo = "https://photo"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    res_create_user = create_user(name=name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=name, password=password)
    jwt_headers_artist = get_user_jwt_header(username=artista, password=password)

    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    genre = "Pop"
    photo = "https://photo"

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers_artist,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_patch_user = patch_history_playback(
        user_name=name, song_name=song_name, headers=jwt_headers_user
    )
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_get_user = get_user(name=name, headers=jwt_headers_user)
    assert res_get_user.status_code == HTTP_200_OK
    assert len(res_get_user.json()["playback_history"]) == 1
    assert res_get_user.json()["playback_history"][0] == song_name

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_patch_playback_history_artist_correct(clear_test_data_db):
    photo = "https://photo"
    password = "hola"
    artista = "artista"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    genre = "Pop"
    photo = "https://photo"

    jwt_headers_artist = get_user_jwt_header(username=artista, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers_artist,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_patch_user = patch_history_playback(artista, song_name, headers=jwt_headers_artist)
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_get_artist = get_artist(name=artista, headers=jwt_headers_artist)
    assert res_get_artist.status_code == HTTP_200_OK
    assert len(res_get_artist.json()["playback_history"]) == 1
    assert res_get_artist.json()["playback_history"][0] == song_name

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_patch_playback_history_non_existing_user():
    photo = "https://photo"
    password = "hola"
    artista = "artista"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_artist = get_user_jwt_header(username=artista, password=password)

    res_patch_user = patch_history_playback("usuario1", "cancion1", jwt_headers_artist)
    assert res_patch_user.status_code == HTTP_404_NOT_FOUND

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_patch_playback_history_user_modifying_another_user():
    photo = "https://photo"
    password = "hola"
    artista = "artista"
    artista2 = "artista2"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    res_create_artist = create_artist(name=artista2, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_artist = get_user_jwt_header(username=artista, password=password)

    res_patch_user = patch_history_playback(artista2, "cancion1", jwt_headers_artist)
    assert res_patch_user.status_code == HTTP_403_FORBIDDEN

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artista2)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_patch_playback_history_song_not_found():
    photo = "https://photo"
    password = "hola"
    artista = "artista"
    photo = "https://photo"
    password = "hola"
    non_existent_song = "non_existent_song"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_artist = get_user_jwt_header(username=artista, password=password)

    res_patch_user = patch_history_playback(artista, non_existent_song, jwt_headers_artist)
    assert res_patch_user.status_code == HTTP_404_NOT_FOUND

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_patch_playback_history_user_correct_insert_6_songs(clear_test_data_db):
    name = "8232392323623823723"
    photo = "https://photo"
    password = "hola"

    res_create_user = create_user(name=name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    genre = "Pop"

    new_song_name = "cancionnueva"

    artista = "artista"
    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=name, password=password)
    jwt_headers_artist = get_user_jwt_header(username=artista, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers_artist,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_create_song = create_song(
        name=new_song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers_artist,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    for i in range(0, 5):
        res_patch_user = patch_history_playback(name, song_name, headers=jwt_headers_user)
        assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_patch_user = patch_history_playback(name, new_song_name, headers=jwt_headers_user)
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_get_user = get_user(name=name, headers=jwt_headers_user)
    assert res_get_user.status_code == HTTP_200_OK
    assert len(res_get_user.json()["playback_history"]) == MAX_NUMBER_PLAYBACK_HISTORY_SONGS
    assert res_get_user.json()["playback_history"][4] == new_song_name

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_song = delete_song(new_song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_patch_saved_playlist_user_correct(clear_test_data_db):
    playlist_name = "playlist"
    user_name = "8232392323623823723"
    description = "descripcion"
    password = "hola"
    photo = "https://photo"

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_create_playlist = create_playlist(
        name=playlist_name, descripcion=description, photo=photo, headers=jwt_headers_user
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_patch_user = patch_playlist_saved(
        user_name=user_name, playlist_name=playlist_name, headers=jwt_headers_user
    )
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_get_user = get_user(name=user_name, headers=jwt_headers_user)
    assert res_get_user.status_code == HTTP_200_OK
    assert len(res_get_user.json()["saved_playlists"]) == 1
    assert res_get_user.json()["saved_playlists"][0] == playlist_name

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


# TODO test_patch_saved_playlist_user_correct for updating playlist name


def test_patch_saved_playlist_user_not_found(clear_test_data_db):
    playlist_name = "playlist"
    user_name = "8232392323623823723"
    description = "descripcion"
    password = "hola"
    photo = "https://photo"

    non_existent_user = "non_existent_user"

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_create_playlist = create_playlist(
        name=playlist_name, descripcion=description, photo=photo, headers=jwt_headers_user
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_patch_user = patch_playlist_saved(
        user_name=non_existent_user, playlist_name=playlist_name, headers=jwt_headers_user
    )
    assert res_patch_user.status_code == HTTP_404_NOT_FOUND

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_patch_saved_playlist_not_found(clear_test_data_db):
    non_existent_playlist_name = "playlist"
    user_name = "8232392323623823723"
    password = "hola"
    photo = "https://photo"

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_patch_user = patch_playlist_saved(
        user_name=user_name,
        playlist_name=non_existent_playlist_name,
        headers=jwt_headers_user,
    )
    assert res_patch_user.status_code == HTTP_404_NOT_FOUND

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_patch_saved_playlist_artist_correct(clear_test_data_db):
    playlist_name = "playlist"
    description = "descripcion"
    password = "hola"
    artista = "artista"
    photo = "https://photo"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=artista, password=password)

    res_create_playlist = create_playlist(playlist_name, description, photo, jwt_headers_user)
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_patch_user = patch_playlist_saved(artista, playlist_name, jwt_headers_user)
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_get_artist = get_artist(name=artista, headers=jwt_headers_user)
    assert res_get_artist.status_code == HTTP_200_OK
    assert len(res_get_artist.json()["saved_playlists"]) == 1
    assert res_get_artist.json()["saved_playlists"][0] == playlist_name

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(artista)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_delete_saved_playlist_artist_correct(clear_test_data_db):
    playlist_name = "playlist"
    description = "descripcion"
    password = "hola"
    artista = "artista"
    photo = "https://photo"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=artista, password=password)

    res_create_playlist = create_playlist(
        playlist_name, description, photo, headers=jwt_headers_user
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_patch_user = patch_playlist_saved(artista, playlist_name, jwt_headers_user)
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_delete_saved_playlist = delete_playlist_saved(
        user_name=artista, playlist_name=playlist_name, headers=jwt_headers_user
    )
    assert res_delete_saved_playlist.status_code == HTTP_202_ACCEPTED

    res_get_artist = get_artist(name=artista, headers=jwt_headers_user)
    assert res_get_artist.status_code == HTTP_200_OK
    assert len(res_get_artist.json()["saved_playlists"]) == 0

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(artista)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_delete_saved_playlist_user_invalid():
    playlist_name = "playlist"
    password = "hola"
    artista = "artista"
    photo = "https://photo"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=artista, password=password)

    res_delete_saved_playlist = delete_playlist_saved(
        user_name=artista, playlist_name=playlist_name, headers=jwt_headers_user
    )
    assert res_delete_saved_playlist.status_code == HTTP_404_NOT_FOUND


def test_delete_saved_playlist_user_correct(clear_test_data_db):
    playlist_name = "playlist"
    user_name = "8232392323623823723"
    description = "descripcion"
    password = "hola"
    photo = "https://photo"

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_create_playlist = create_playlist(playlist_name, description, photo, jwt_headers_user)
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_patch_user = patch_playlist_saved(user_name, playlist_name, jwt_headers_user)
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_delete_saved_playlist = delete_playlist_saved(
        user_name=user_name, playlist_name=playlist_name, headers=jwt_headers_user
    )
    assert res_delete_saved_playlist.status_code == HTTP_202_ACCEPTED

    res_get_user = get_user(name=user_name, headers=jwt_headers_user)
    assert res_get_user.status_code == HTTP_200_OK
    assert len(res_get_user.json()["saved_playlists"]) == 0

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_delete_saved_playlist_user_not_found(clear_test_data_db):
    playlist_name = "playlist"
    user_name = "8232392323623823723"
    description = "descripcion"
    password = "hola"
    photo = "https://photo"
    non_existent_user_name = "non_existent_user_name"

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_create_playlist = create_playlist(playlist_name, description, photo, jwt_headers_user)
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_delete_saved_playlist = delete_playlist_saved(
        user_name=non_existent_user_name, playlist_name=playlist_name, headers=jwt_headers_user
    )
    assert res_delete_saved_playlist.status_code == HTTP_404_NOT_FOUND

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_delete_saved_playlist_user_modifying_another_user(clear_test_data_db):
    playlist_name = "playlist"
    user_name = "8232392323623823723"
    user_name2 = "user-name2"
    description = "descripcion"
    password = "hola"
    photo = "https://photo"

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    res_create_user = create_user(name=user_name2, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    jwt_headers_user2 = get_user_jwt_header(username=user_name2, password=password)

    res_create_playlist = create_playlist(playlist_name, description, photo, jwt_headers_user)
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_delete_saved_playlist = delete_playlist_saved(
        user_name=user_name,
        playlist_name=playlist_name,
        headers=jwt_headers_user2,
    )
    assert res_delete_saved_playlist.status_code == HTTP_403_FORBIDDEN

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_whoami_artist(clear_test_data_db):
    password = "hola"
    artista = "artista"
    photo = "https://photo"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    res_login_artist = post_login(artista, password)
    assert res_login_artist.status_code == HTTP_200_OK

    jwt = res_login_artist.json()

    res_whoami = whoami(jwt)
    assert res_whoami.status_code == HTTP_200_OK

    assert res_whoami.json()["username"] == artista
    assert res_whoami.json()["token_type"] == "bearer"
    assert res_whoami.json()["role"] == UserType.ARTIST.value

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_whoami_user(clear_test_data_db):
    user_name = "8232392323623823723"
    password = "hola"
    photo = "https://photo"

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    res_login_user = post_login(user_name, password)
    assert res_login_user.status_code == HTTP_200_OK

    jwt = res_login_user.json()

    res_whoami = whoami(jwt)
    assert res_whoami.status_code == HTTP_200_OK

    assert res_whoami.json()["username"] == user_name
    assert res_whoami.json()["token_type"] == "bearer"
    assert res_whoami.json()["role"] == UserType.USER.value

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_whoami_invalid_jwt(clear_test_data_db):
    res_whoami = whoami("")
    assert res_whoami.status_code == HTTP_403_FORBIDDEN


def test_add_playlist_to_owner_user_correct(clear_test_data_db):
    playlist_name = "playlist"
    user_name = "8232392323623823723"
    description = "descripcion"
    password = "hola"
    photo = "https://photo"

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_create_playlist = create_playlist(playlist_name, description, photo, jwt_headers_user)
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_get_user = get_user(name=user_name, headers=jwt_headers_user)
    assert res_get_user.status_code == HTTP_200_OK
    assert len(res_get_user.json()["playlists"]) == 1
    assert res_get_user.json()["playlists"][0] == playlist_name

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_add_playlist_to_owner_user_invalid(clear_test_data_db):
    playlist_name = "playlist"
    description = "descripcion"
    photo = "https://photo"

    res_create_playlist = create_playlist(playlist_name, description, photo, {})
    assert res_create_playlist.status_code == HTTP_403_FORBIDDEN


def test_add_playlist_to_owner_artist_correct(clear_test_data_db):
    playlist_name = "playlist"
    user_name = "8232392323623823723"
    description = "descripcion"
    password = "hola"
    photo = "https://photo"

    res_create_artist = create_artist(name=user_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_create_playlist = create_playlist(playlist_name, description, photo, jwt_headers_user)
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_get_artist = get_artist(name=user_name, headers=jwt_headers_user)
    assert res_get_artist.status_code == HTTP_200_OK
    assert len(res_get_artist.json()["playlists"]) == 1
    assert res_get_artist.json()["playlists"][0] == playlist_name

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_delete_playlist_from_owner_user_correct(clear_test_data_db):
    playlist_name = "playlist"
    user_name = "8232392323623823723"
    description = "descripcion"
    password = "hola"
    photo = "https://photo"

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_create_playlist = create_playlist(playlist_name, description, photo, jwt_headers_user)
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_get_user = get_user(name=user_name, headers=jwt_headers_user)
    assert res_get_user.status_code == HTTP_200_OK
    assert len(res_get_user.json()["playlists"]) == 1
    assert res_get_user.json()["playlists"][0] == playlist_name

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_delete_playlist_from_owner_artist_correct(clear_test_data_db):
    playlist_name = "playlist"
    user_name = "8232392323623823723"
    description = "descripcion"
    password = "hola"
    photo = "https://photo"

    res_create_artist = create_artist(name=user_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_create_playlist = create_playlist(playlist_name, description, photo, jwt_headers_user)
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_get_artist = get_artist(name=user_name, headers=jwt_headers_user)
    assert res_get_artist.status_code == HTTP_200_OK
    assert len(res_get_artist.json()["playlists"]) == 1
    assert res_get_artist.json()["playlists"][0] == playlist_name

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_get_user_relevant_playlist_correct():
    playlist_name_user = "playlist"
    playlist_name_artist_saved = "saved-playlist"
    user_name = "user-name"
    artist_name = "artist-name"
    description = "description"
    password = "pass"
    photo = "https://photo"

    expected_relevant_playlists = 2

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)
    jwt_headers_artist = get_user_jwt_header(username=artist_name, password=password)

    res_create_playlist = create_playlist(
        playlist_name_user, description, photo, jwt_headers_user
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_create_playlist = create_playlist(
        playlist_name_artist_saved, description, photo, jwt_headers_artist
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_patch_user = patch_playlist_saved(
        user_name=user_name,
        playlist_name=playlist_name_artist_saved,
        headers=jwt_headers_user,
    )
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_get_user_relevant_playlists = get_user_relevant_playlists(user_name, jwt_headers_user)
    assert res_get_user_relevant_playlists.status_code == HTTP_200_OK
    assert len(res_get_user_relevant_playlists.json()) == expected_relevant_playlists

    res_delete_playlist = delete_playlist(playlist_name_user)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_playlist = delete_playlist(playlist_name_artist_saved)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_artist_relevant_playlist_correct():
    playlist_name_user_saved = "playlist"
    playlist_name_artist = "saved-playlist"
    user_name = "user-name"
    artist_name = "artist-name"
    description = "description"
    password = "pass"
    photo = "https://photo"

    expected_relevant_playlists = 2

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)
    jwt_headers_artist = get_user_jwt_header(username=artist_name, password=password)

    res_create_playlist = create_playlist(
        playlist_name_user_saved, description, photo, jwt_headers_user
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_create_playlist = create_playlist(
        playlist_name_artist, description, photo, jwt_headers_artist
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_patch_user = patch_playlist_saved(
        user_name=artist_name,
        playlist_name=playlist_name_user_saved,
        headers=jwt_headers_artist,
    )
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_get_artist_relevant_playlists = get_user_relevant_playlists(
        artist_name, jwt_headers_artist
    )
    assert res_get_artist_relevant_playlists.status_code == HTTP_200_OK
    assert len(res_get_artist_relevant_playlists.json()) == expected_relevant_playlists

    res_delete_playlist = delete_playlist(playlist_name_user_saved)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_playlist = delete_playlist(playlist_name_artist)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_user_relevant_playlist_user_not_found():
    user_name = "user-name"
    artist_name = "artist-name"
    password = "pass"
    photo = "https://photo"

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_artist = get_user_jwt_header(username=artist_name, password=password)

    res_get_user_relevant_playlists = get_user_relevant_playlists(
        user_name, jwt_headers_artist
    )
    assert res_get_user_relevant_playlists.status_code == HTTP_404_NOT_FOUND

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_user_playlist_names_correct():
    playlist_name_user = "playlist"
    playlist_name_artist_saved = "saved-playlist"
    user_name = "user-name"
    artist_name = "artist-name"
    description = "description"
    password = "pass"
    photo = "https://photo"

    expected_user_playlist_names = [playlist_name_user]
    expected_amount_user_playlist_names = len(expected_user_playlist_names)

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)
    jwt_headers_artist = get_user_jwt_header(username=artist_name, password=password)

    res_create_playlist = create_playlist(
        playlist_name_user, description, photo, jwt_headers_user
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_create_playlist = create_playlist(
        playlist_name_artist_saved, description, photo, jwt_headers_artist
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_patch_user = patch_playlist_saved(
        user_name=user_name,
        playlist_name=playlist_name_artist_saved,
        headers=jwt_headers_user,
    )
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_get_user_playlist_names = get_user_playlist_names(user_name, jwt_headers_user)
    assert res_get_user_playlist_names.status_code == HTTP_200_OK
    assert len(res_get_user_playlist_names.json()) == expected_amount_user_playlist_names
    assert set(expected_user_playlist_names) == set(res_get_user_playlist_names.json())

    res_delete_playlist = delete_playlist(playlist_name_user)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_playlist = delete_playlist(playlist_name_artist_saved)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_artist_playlist_names_correct():
    playlist_name_user_saved = "playlist"
    playlist_name_artist = "saved-playlist"
    user_name = "user-name"
    artist_name = "artist-name"
    description = "description"
    password = "pass"
    photo = "https://photo"

    expected_user_playlist_names = [playlist_name_artist]
    expected_amount_user_playlist_names = len(expected_user_playlist_names)

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)
    jwt_headers_artist = get_user_jwt_header(username=artist_name, password=password)

    res_create_playlist = create_playlist(
        playlist_name_user_saved, description, photo, jwt_headers_user
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_create_playlist = create_playlist(
        playlist_name_artist, description, photo, jwt_headers_artist
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_patch_user = patch_playlist_saved(
        user_name=artist_name,
        playlist_name=playlist_name_user_saved,
        headers=jwt_headers_artist,
    )
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_get_artist_playlist_names = get_user_playlist_names(artist_name, jwt_headers_artist)
    assert res_get_artist_playlist_names.status_code == HTTP_200_OK
    assert len(res_get_artist_playlist_names.json()) == expected_amount_user_playlist_names
    assert set(expected_user_playlist_names) == set(res_get_artist_playlist_names.json())

    res_delete_playlist = delete_playlist(playlist_name_user_saved)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_playlist = delete_playlist(playlist_name_artist)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_user_playlist_names_user_not_found():
    user_name = "user-name"
    artist_name = "artist-name"
    password = "pass"
    photo = "https://photo"

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_artist = get_user_jwt_header(username=artist_name, password=password)

    res_get_user_playlist_names = get_user_playlist_names(user_name, jwt_headers_artist)
    assert res_get_user_playlist_names.status_code == HTTP_404_NOT_FOUND

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_user_playlists_correct():
    playlist_name_user = "playlist"
    playlist_name_artist_saved = "saved-playlist"
    user_name = "user-name"
    artist_name = "artist-name"
    description = "description"
    password = "pass"
    photo = "https://photo"

    expected_user_playlist_names = [playlist_name_user]
    expected_amount_user_playlist_names = len(expected_user_playlist_names)

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)
    jwt_headers_artist = get_user_jwt_header(username=artist_name, password=password)

    res_create_playlist = create_playlist(
        playlist_name_user, description, photo, jwt_headers_user
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_create_playlist = create_playlist(
        playlist_name_artist_saved, description, photo, jwt_headers_artist
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_patch_user = patch_playlist_saved(
        user_name=user_name,
        playlist_name=playlist_name_artist_saved,
        headers=jwt_headers_user,
    )
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_get_user_playlist_names = get_user_playlists(user_name, jwt_headers_user)
    assert res_get_user_playlist_names.status_code == HTTP_200_OK
    assert len(res_get_user_playlist_names.json()) == expected_amount_user_playlist_names
    assert set(expected_user_playlist_names) == set(
        [playlist["name"] for playlist in res_get_user_playlist_names.json()]
    )

    res_delete_playlist = delete_playlist(playlist_name_user)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_playlist = delete_playlist(playlist_name_artist_saved)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_artist_playlists_correct():
    playlist_name_user_saved = "playlist"
    playlist_name_artist = "saved-playlist"
    user_name = "user-name"
    artist_name = "artist-name"
    description = "description"
    password = "pass"
    photo = "https://photo"

    excepted_playback_history_songs = [playlist_name_artist]
    expected_amount_user_playlist_names = len(excepted_playback_history_songs)

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)
    jwt_headers_artist = get_user_jwt_header(username=artist_name, password=password)

    res_create_playlist = create_playlist(
        playlist_name_user_saved, description, photo, jwt_headers_user
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_create_playlist = create_playlist(
        playlist_name_artist, description, photo, jwt_headers_artist
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_patch_user = patch_playlist_saved(
        user_name=artist_name,
        playlist_name=playlist_name_user_saved,
        headers=jwt_headers_artist,
    )
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_get_artist_playlist_names = get_user_playlists(artist_name, jwt_headers_artist)
    assert res_get_artist_playlist_names.status_code == HTTP_200_OK
    assert len(res_get_artist_playlist_names.json()) == expected_amount_user_playlist_names
    assert set(excepted_playback_history_songs) == set(
        [playlist["name"] for playlist in res_get_artist_playlist_names.json()]
    )

    res_delete_playlist = delete_playlist(playlist_name_user_saved)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_playlist = delete_playlist(playlist_name_artist)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_user_playlists_user_not_found():
    user_name = "user-name"
    artist_name = "artist-name"
    password = "pass"
    photo = "https://photo"

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_artist = get_user_jwt_header(username=artist_name, password=password)

    res_get_user_playlist_names = get_user_playlists(user_name, jwt_headers_artist)
    assert res_get_user_playlist_names.status_code == HTTP_404_NOT_FOUND

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_user_playback_history_correct():
    artist_name = "artist-name"
    password = "pass"
    photo = "https://photo"
    song_name = "8232392323623823723989"
    song_name_2 = "8232392323623823723988"
    excepted_playback_history_songs = [song_name, song_name_2]
    file_path = "tests/assets/song.mp3"
    genre = "Pop"

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_artist = get_user_jwt_header(username=artist_name, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers_artist,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_create_song = create_song(
        name=song_name_2,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers_artist,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_patch_user = patch_history_playback(
        user_name=artist_name, song_name=song_name, headers=jwt_headers_artist
    )
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_patch_user = patch_history_playback(
        user_name=artist_name, song_name=song_name_2, headers=jwt_headers_artist
    )
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_get_user_playback_history = get_user_playback_history(
        artist_name, headers=jwt_headers_artist
    )
    assert res_get_user_playback_history.status_code == HTTP_200_OK
    assert set(excepted_playback_history_songs) == set(
        [song["name"] for song in res_get_user_playback_history.json()]
    )

    delete_song(name=song_name)
    delete_song(name=song_name_2)

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_user_playback_history_user_not_found():
    artist_name = "artist-name"
    password = "pass"
    photo = "https://photo"

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_artist = get_user_jwt_header(username=artist_name, password=password)

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED

    res_get_user_playback_history = get_user_playback_history(
        artist_name, headers=jwt_headers_artist
    )
    assert res_get_user_playback_history.status_code == HTTP_404_NOT_FOUND


def test_get_base_user_dao_from_document():
    user_name = "user-name"
    user_photo = "https://photo"
    user_register_date = "2024-11-30T10:00:00Z"
    user_password: bytes = b"pass"

    document = {
        "name": user_name,
        "photo": user_photo,
        "register_date": user_register_date,
        "password": user_password,
    }

    document = BaseUserDocument(
        name=user_name,
        photo=user_photo,
        register_date=user_register_date,
        password=bytes(user_password),
    )

    res_base_user_dao = get_base_user_dao_from_document(document)

    assert isinstance(res_base_user_dao, BaseUserDAO)
    assert res_base_user_dao.name == user_name
    assert res_base_user_dao.photo == user_photo
    assert res_base_user_dao.register_date == user_register_date[:-1]
    assert res_base_user_dao.password == user_password


def test_get_base_user_dto_from_dao():
    user_name = "user-name"
    user_photo = "https://photo"
    user_register_date = "2024-11-30T10:00:00Z"

    base_user_dao = BaseUserDAO(
        name=user_name, photo=user_photo, register_date=user_register_date, password=b"pass"
    )

    res_base_user_dto = get_base_user_dto_from_dao(base_user_dao)

    assert isinstance(res_base_user_dto, BaseUserDTO)
    assert res_base_user_dto.name == user_name
    assert res_base_user_dto.photo == user_photo
    assert res_base_user_dto.register_date == user_register_date


def test_promote_user_to_artist_correct():
    user_name = "user-to-promote"
    password = "password"
    photo = "https://photo"

    # Create a user
    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED
    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_get_user = get_user(name=user_name, headers=jwt_headers_user)
    assert res_get_user.status_code == HTTP_200_OK
    assert res_get_user.json()["name"] == user_name
    assert res_get_user.json()["photo"] == photo

    # Promote the user to artist
    res_promote_user = promote_user_to_artist(name=user_name, headers=jwt_headers_user)
    assert res_promote_user.status_code == HTTP_204_NO_CONTENT

    # Verify the user is promoted to artist
    jwt_headers_artist = get_user_jwt_header(username=user_name, password=password)

    res_get_artist = get_artist(name=user_name, headers=jwt_headers_artist)
    assert res_get_artist.status_code == HTTP_200_OK
    assert res_get_artist.json()["name"] == user_name
    assert res_get_artist.json()["photo"] == photo

    # Clean up
    res_delete_artist = delete_user(name=user_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_promote_user_to_artist_user_not_found(clear_test_data_db):
    user_name = "8232392323623823723"
    password = "pass"
    photo = "http://photo"

    res_create_user = create_user(user_name, photo, password)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    # Test promote nonexistent user
    res_promote_user = promote_user_to_artist("non_existent_user", jwt_headers_user)
    assert res_promote_user.status_code == HTTP_404_NOT_FOUND


def test_promote_user_to_artist_invalid(clear_test_data_db):
    user_name = "8232392323623823723"
    password = "pass"
    photo = "http://photo"

    res_create_user = create_user(user_name, photo, password)
    assert res_create_user.status_code == HTTP_201_CREATED

    # Test promoting without auth
    res_promote_user = promote_user_to_artist(user_name, {})
    assert res_promote_user.status_code == HTTP_403_FORBIDDEN


def test_promote_user_to_artist_another_user(clear_test_data_db):
    user_name = "8232392323623823723"
    password = "pass"
    photo = "http://photo"

    res_create_user = create_user(user_name, photo, password)
    assert res_create_user.status_code == HTTP_201_CREATED

    # Test promoting another user
    other_user = "other_user"
    res_create_other = create_user(other_user, photo, password)
    assert res_create_other.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(user_name, password)

    res_promote_other = promote_user_to_artist(other_user, jwt_headers_user)
    assert res_promote_other.status_code == HTTP_403_FORBIDDEN

    res_delete_other = delete_user(other_user)
    assert res_delete_other.status_code == HTTP_202_ACCEPTED


@mark.asyncio
async def test_promote_user_to_artist_already_exists(clear_test_data_db):
    artist = {
        "name": "artista",
        "photo": "http://photo",
        "current_date": get_current_iso8601_date(),
        "password": auth_service.hash_password("password"),
    }
    user_name = "artista"
    password = "password"
    photo = "http://photo"

    res_create_user = create_user(user_name, photo, password)
    assert res_create_user.status_code == HTTP_201_CREATED

    await create_artist_repo(**artist)

    jwt_headers_user = get_user_jwt_header(user_name, password)

    res_promote_other = promote_user_to_artist(user_name, jwt_headers_user)
    assert res_promote_other.status_code == HTTP_400_BAD_REQUEST


# executes after all tests
@fixture()
def clear_test_data_db():
    name = "8232392323623823723"
    song_name = "8232392323623823723989"
    new_song_name = "cancionnueva"
    artista = "artista"

    delete_user(name=name)
    delete_user(name=artista)
    delete_song(name=song_name)
    delete_song(name=new_song_name)

    yield
    name = "8232392323623823723"
    song_name = "8232392323623823723989"
    new_song_name = "cancionnueva"
    artista = "artista"

    delete_user(name=name)
    delete_user(name=artista)
    delete_song(name=song_name)
    delete_song(name=new_song_name)
