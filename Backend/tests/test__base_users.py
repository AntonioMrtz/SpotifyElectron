from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from test_API.api_all_users import (
    delete_playlist_saved,
    patch_history_playback,
    patch_playlist_saved,
    whoami,
)
from test_API.api_login import post_login
from test_API.api_test_artist import create_artist, get_artist
from test_API.api_test_playlist import create_playlist, delete_playlist
from test_API.api_test_song import create_song, delete_song
from test_API.api_test_user import create_user, delete_user, get_user
from test_API.api_token import get_user_jwt_header

from app.spotify_electron.user.base_user_service import (
    MAX_NUMBER_PLAYBACK_HISTORY_SONGS,
)
from app.spotify_electron.user.user.user_schema import UserType


@fixture(scope="module", autouse=True)
def set_up(trigger_app_start):
    pass


def test_patch_playback_history_user_correct(clear_test_data_db):
    name = "8232392323623823723"
    password = "hola"
    artista = "artista"
    foto = "https://foto"

    res_create_artist = create_artist(name=artista, password=password, photo=foto)
    assert res_create_artist.status_code == HTTP_201_CREATED

    res_create_user = create_user(name=name, password=password, photo=foto)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=name, password=password)
    jwt_headers_artist = get_user_jwt_header(username=artista, password=password)

    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    genero = "Pop"
    foto = "https://foto"

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genero,
        photo=foto,
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
    foto = "https://foto"
    password = "hola"
    artista = "artista"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=foto)
    assert res_create_artist.status_code == HTTP_201_CREATED

    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    genero = "Pop"
    foto = "https://foto"

    jwt_headers_artist = get_user_jwt_header(username=artista, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genero,
        photo=foto,
        headers=jwt_headers_artist,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_patch_user = patch_history_playback(
        artista, song_name, headers=jwt_headers_artist
    )
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_get_artist = get_artist(name=artista, headers=jwt_headers_artist)
    assert res_get_artist.status_code == HTTP_200_OK
    assert len(res_get_artist.json()["playback_history"]) == 1
    assert res_get_artist.json()["playback_history"][0] == song_name

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_patch_playback_history_invalid_bad_user():
    foto = "https://foto"
    password = "hola"
    artista = "artista"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=foto)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_artist = get_user_jwt_header(username=artista, password=password)

    res_patch_user = patch_history_playback("", "", headers=jwt_headers_artist)
    assert res_patch_user.status_code == HTTP_404_NOT_FOUND

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_patch_playback_history_non_existing_user():
    res_patch_user = patch_history_playback("usuario1", "cancion1", {})
    assert res_patch_user.status_code == HTTP_401_UNAUTHORIZED


def test_patch_playback_history_user_correct_insert_6_songs(clear_test_data_db):
    name = "8232392323623823723"
    foto = "https://foto"
    password = "hola"

    res_create_user = create_user(name=name, password=password, photo=foto)
    assert res_create_user.status_code == HTTP_201_CREATED

    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    genero = "Pop"

    new_song_name = "cancionnueva"

    artista = "artista"
    res_create_artist = create_artist(name=artista, password=password, photo=foto)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=name, password=password)
    jwt_headers_artist = get_user_jwt_header(username=artista, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genero,
        photo=foto,
        headers=jwt_headers_artist,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_create_song = create_song(
        name=new_song_name,
        file_path=file_path,
        genre=genero,
        photo=foto,
        headers=jwt_headers_artist,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    for i in range(0, 5):
        res_patch_user = patch_history_playback(
            name, song_name, headers=jwt_headers_user
        )
        assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_patch_user = patch_history_playback(
        name, new_song_name, headers=jwt_headers_user
    )
    assert res_patch_user.status_code == HTTP_204_NO_CONTENT

    res_get_user = get_user(name=name, headers=jwt_headers_user)
    assert res_get_user.status_code == HTTP_200_OK
    assert (
        len(res_get_user.json()["playback_history"])
        == MAX_NUMBER_PLAYBACK_HISTORY_SONGS
    )
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
    foto = "https://foto"

    res_create_user = create_user(name=user_name, password=password, photo=foto)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_create_playlist = create_playlist(
        name=playlist_name, descripcion=description, foto=foto, headers=jwt_headers_user
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


def test_patch_saved_playlist_user_not_found():
    res_patch_user = patch_playlist_saved("", "", {})
    assert res_patch_user.status_code in (HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED)


def test_patch_saved_playlist_artist_correct(clear_test_data_db):
    playlist_name = "playlist"
    description = "descripcion"
    password = "hola"
    artista = "artista"
    foto = "https://foto"

    res_create_artist = create_artist(name=artista, password=password, photo=foto)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=artista, password=password)

    res_create_playlist = create_playlist(
        playlist_name, description, foto, jwt_headers_user
    )
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
    foto = "https://foto"

    res_create_artist = create_artist(name=artista, password=password, photo=foto)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=artista, password=password)

    res_create_playlist = create_playlist(
        playlist_name, description, foto, headers=jwt_headers_user
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
    foto = "https://foto"

    res_create_artist = create_artist(name=artista, password=password, photo=foto)
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
    foto = "https://foto"

    res_create_user = create_user(name=user_name, password=password, photo=foto)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_create_playlist = create_playlist(
        playlist_name, description, foto, jwt_headers_user
    )
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


def test_whoami_artist(clear_test_data_db):
    password = "hola"
    artista = "artista"
    foto = "https://foto"

    res_create_artist = create_artist(name=artista, password=password, photo=foto)
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
    foto = "https://foto"

    res_create_user = create_user(name=user_name, password=password, photo=foto)
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


def test_whoami_jwt_invalid():
    res_whoami = whoami("jwt invalid")
    assert res_whoami.status_code == HTTP_401_UNAUTHORIZED


def test_add_playlist_to_owner_user_correct(clear_test_data_db):
    playlist_name = "playlist"
    user_name = "8232392323623823723"
    description = "descripcion"
    password = "hola"
    foto = "https://foto"

    res_create_user = create_user(name=user_name, password=password, photo=foto)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_create_playlist = create_playlist(
        playlist_name, description, foto, jwt_headers_user
    )
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
    foto = "https://foto"

    res_create_playlist = create_playlist(playlist_name, description, foto, {})
    assert res_create_playlist.status_code == HTTP_401_UNAUTHORIZED


def test_add_playlist_to_owner_artist_correct(clear_test_data_db):
    playlist_name = "playlist"
    user_name = "8232392323623823723"
    description = "descripcion"
    password = "hola"
    foto = "https://foto"

    res_create_artist = create_artist(name=user_name, password=password, photo=foto)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_create_playlist = create_playlist(
        playlist_name, description, foto, jwt_headers_user
    )
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
    foto = "https://foto"

    res_create_user = create_user(name=user_name, password=password, photo=foto)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_create_playlist = create_playlist(
        playlist_name, description, foto, jwt_headers_user
    )
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
    foto = "https://foto"

    res_create_artist = create_artist(name=user_name, password=password, photo=foto)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers_user = get_user_jwt_header(username=user_name, password=password)

    res_create_playlist = create_playlist(
        playlist_name, description, foto, jwt_headers_user
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_get_artist = get_artist(name=user_name, headers=jwt_headers_user)
    assert res_get_artist.status_code == HTTP_200_OK
    assert len(res_get_artist.json()["playlists"]) == 1
    assert res_get_artist.json()["playlists"][0] == playlist_name

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


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
