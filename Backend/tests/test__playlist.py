from datetime import datetime

import pytest
from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)

from tests.test_API.api_base_users import patch_playlist_saved
from tests.test_API.api_test_artist import create_artist
from tests.test_API.api_test_playlist import (
    add_songs_to_playlist,
    create_playlist,
    delete_playlist,
    get_playlist,
    get_playlists,
    remove_song_from_playlist,
    update_playlist,
)
from tests.test_API.api_test_song import create_song, delete_song
from tests.test_API.api_test_user import delete_user, get_user
from tests.test_API.api_token import get_user_jwt_header


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


def test_get_playlist_correct():
    name = "8232392323623823723"
    photo = "https://photo"
    descripcion = "hola"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    formatting = "%Y-%m-%dT%H:%M:%S"
    post_date_iso8601 = datetime.strptime(
        datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), formatting
    )

    res_create_artist = create_artist(owner, photo, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=owner, password=password)

    res_create_playlist = create_playlist(
        name=name, descripcion=descripcion, photo=photo, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_get_playlist = get_playlist(name=name, headers=jwt_headers)
    assert res_get_playlist.status_code == HTTP_200_OK
    assert res_get_playlist.json()["name"] == name
    assert res_get_playlist.json()["photo"] == photo
    assert res_get_playlist.json()["description"] == descripcion
    assert res_get_playlist.json()["owner"] == owner

    try:
        fecha = res_get_playlist.json()["upload_date"]
        response_date = datetime.strptime(fecha, formatting)

        assert response_date.hour == post_date_iso8601.hour

    except ValueError:
        assert False

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_playlist_not_found():
    name = "8232392323623823723"

    photo = "https://photo"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, photo, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=owner, password=password)

    res_get_playlist = get_playlist(name=name, headers=jwt_headers)
    assert res_get_playlist.status_code == HTTP_404_NOT_FOUND

    res_create_artist = delete_user(owner)
    assert res_create_artist.status_code == HTTP_202_ACCEPTED


def test_post_playlist_correct():
    name = "8232392323623823723"
    photo = "https://photo"
    descripcion = "hola"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, photo, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=owner, password=password)

    res_create_playlist = create_playlist(
        name=name, descripcion=descripcion, photo=photo, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_delete_playlist_correct():
    name = "8232392323623823723"
    photo = "https://photo"
    descripcion = "hola"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, photo, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=owner, password=password)

    res_create_playlist = create_playlist(
        name=name, descripcion=descripcion, photo=photo, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_delete__playlist_not_found():
    name = "8232392323623823723"

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == HTTP_404_NOT_FOUND


def test_delete_playlist_invalid_name():
    name = ""

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == HTTP_405_METHOD_NOT_ALLOWED


def test_update_playlist_correct():
    name = "8232392323623823723"
    photo = "photo"
    descripcion = "descripcion"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, photo, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=owner, password=password)

    res_create_playlist = create_playlist(
        name=name, descripcion=descripcion, photo=photo, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    new_description = "nuevadescripcion"

    res_update_playlist = update_playlist(
        name=name, photo=photo, descripcion=new_description, headers=jwt_headers
    )
    assert res_update_playlist.status_code == HTTP_204_NO_CONTENT

    res_get_playlist = get_playlist(name=name, headers=jwt_headers)
    assert res_get_playlist.status_code == HTTP_200_OK
    assert res_get_playlist.json()["description"] == new_description

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


@pytest.mark.skip(reason="mongomock don't support the operator playlists.$")
def test_update_playlist_correct_new_name():
    name = "8232392323623823723"
    photo = "photo"
    descripcion = "descripcion"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, photo, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=owner, password=password)

    res_create_playlist = create_playlist(
        name=name, descripcion=descripcion, photo=photo, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_patch_playlist_saved = patch_playlist_saved(
        user_name=owner, playlist_name=name, headers=jwt_headers
    )
    assert res_patch_playlist_saved.status_code == HTTP_204_NO_CONTENT

    new_name = "82323923236238237237"
    new_description = "nuevadescripcion"

    res_update_playlist = update_playlist(
        name=name,
        photo=photo,
        descripcion=new_description,
        nuevo_nombre=new_name,
        headers=jwt_headers,
    )
    assert res_update_playlist.status_code == HTTP_204_NO_CONTENT

    res_get_playlist = get_playlist(new_name, headers=jwt_headers)
    assert res_get_playlist.status_code == HTTP_200_OK

    res_get_user = get_user(owner, jwt_headers)
    assert new_name in res_get_user.json()["playlists"]
    assert new_name in res_get_user.json()["saved_playlists"]

    res_delete_playlist = delete_playlist(new_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_playlists():
    name = "8232392323623823723"
    photo = "photo"
    descripcion = "descripcion"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, photo, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=owner, password=password)

    res_create_playlist = create_playlist(
        name=name, descripcion=descripcion, photo=photo, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    new_name = "82323923236238237237"
    photo = "photo"
    descripcion = "descripcion"

    res_create_playlist = create_playlist(
        name=new_name, descripcion=descripcion, photo=photo, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    expected_number_created_playlists = 2

    res_get_playlists = get_playlists(f"{name},{new_name}", headers=jwt_headers)
    assert res_get_playlists.status_code == HTTP_200_OK
    assert len(res_get_playlists.json()["playlists"]) == expected_number_created_playlists

    res_delete_playlist = delete_playlist(name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_playlist = delete_playlist(new_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_add_songs_to_playlist_correct():
    song_name = "song-name"
    song_name_2 = "song-name-2"
    song_name_3 = "song-name-3"
    file_path = "tests/assets/song.mp3"
    genre = "Pop"
    photo = "https://photo"

    playlist_name = "playlist-name"
    playlist_owner = "playlist-user"
    description = "playlist-description"
    password = "password"

    songs = [song_name, song_name_2, song_name_3]

    res_create_artist = create_artist(playlist_owner, photo, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=playlist_owner, password=password)

    res_create_playlist = create_playlist(
        name=playlist_name, descripcion=description, photo=photo, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    for name in songs:
        res_create_song = create_song(
            name=name,
            file_path=file_path,
            genre=genre,
            photo=photo,
            headers=jwt_headers,
        )
        assert res_create_song.status_code == HTTP_201_CREATED

    res_add_song_to_playlist = add_songs_to_playlist(
        name=playlist_name, song_names=[song_name, song_name_3], headers=jwt_headers
    )
    assert res_add_song_to_playlist.status_code == HTTP_204_NO_CONTENT

    expected_number_playlist_songs = 2

    res_get_playlist = get_playlist(playlist_name, headers=jwt_headers)
    assert res_get_playlist.status_code == HTTP_200_OK
    assert len(res_get_playlist.json()["song_names"]) == expected_number_playlist_songs

    res_add_song_to_playlist = add_songs_to_playlist(
        name=playlist_name, song_names=[song_name_2], headers=jwt_headers
    )
    assert res_add_song_to_playlist.status_code == HTTP_204_NO_CONTENT

    expected_number_playlist_songs = 3

    res_get_playlist = get_playlist(playlist_name, headers=jwt_headers)
    assert res_get_playlist.status_code == HTTP_200_OK
    assert len(res_get_playlist.json()["song_names"]) == expected_number_playlist_songs

    for name in songs:
        res_delete_song = delete_song(name)
        assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(playlist_owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_add_songs_to_playlist_playlist_not_found():
    song_name = "song-name"
    file_path = "tests/assets/song.mp3"
    genre = "Pop"
    photo = "https://photo"

    playlist_name = "playlist-name"
    playlist_owner = "playlist-user"
    password = "password"

    res_create_artist = create_artist(playlist_owner, photo, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=playlist_owner, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_add_song_to_playlist = add_songs_to_playlist(
        name=playlist_name, song_names=[song_name], headers=jwt_headers
    )
    assert res_add_song_to_playlist.status_code == HTTP_404_NOT_FOUND

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(playlist_owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_add_songs_to_playlist_song_not_found():
    song_name = "song-name"
    photo = "https://photo"

    playlist_name = "playlist-name"
    playlist_owner = "playlist-user"
    description = "playlist-description"
    password = "password"

    res_create_artist = create_artist(playlist_owner, photo, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=playlist_owner, password=password)

    res_create_playlist = create_playlist(
        name=playlist_name, descripcion=description, photo=photo, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_add_song_to_playlist = add_songs_to_playlist(
        name=playlist_name, song_names=[song_name], headers=jwt_headers
    )
    assert res_add_song_to_playlist.status_code == HTTP_404_NOT_FOUND

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(playlist_owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_remove_song_from_playlist_correct():
    song_name = "song-name"
    song_name_2 = "song-name-2"
    song_name_3 = "song-name-3"
    file_path = "tests/assets/song.mp3"
    genre = "Pop"
    photo = "https://photo"

    playlist_name = "playlist-name"
    playlist_owner = "playlist-user"
    description = "playlist-description"
    password = "password"

    songs = [song_name, song_name_2, song_name_3]

    res_create_artist = create_artist(playlist_owner, photo, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=playlist_owner, password=password)

    res_create_playlist = create_playlist(
        name=playlist_name, descripcion=description, photo=photo, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    for name in songs:
        res_create_song = create_song(
            name=name,
            file_path=file_path,
            genre=genre,
            photo=photo,
            headers=jwt_headers,
        )
        assert res_create_song.status_code == HTTP_201_CREATED

    res_add_song_to_playlist = add_songs_to_playlist(
        name=playlist_name,
        song_names=[song_name, song_name_2, song_name_3],
        headers=jwt_headers,
    )
    assert res_add_song_to_playlist.status_code == HTTP_204_NO_CONTENT

    res_remove_song_to_playlist = remove_song_from_playlist(
        name=playlist_name, song_names=[song_name, song_name_2], headers=jwt_headers
    )
    assert res_remove_song_to_playlist.status_code == HTTP_202_ACCEPTED

    expected_number_playlist_songs = 1

    res_get_playlist = get_playlist(playlist_name, headers=jwt_headers)
    assert res_get_playlist.status_code == HTTP_200_OK
    assert len(res_get_playlist.json()["song_names"]) == expected_number_playlist_songs

    res_remove_song_to_playlist = remove_song_from_playlist(
        name=playlist_name, song_names=[song_name_3], headers=jwt_headers
    )
    assert res_remove_song_to_playlist.status_code == HTTP_202_ACCEPTED

    expected_number_playlist_songs = 0

    res_get_playlist = get_playlist(playlist_name, headers=jwt_headers)
    assert res_get_playlist.status_code == HTTP_200_OK
    assert len(res_get_playlist.json()["song_names"]) == expected_number_playlist_songs

    for name in songs:
        res_delete_song = delete_song(name)
        assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(playlist_owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_remove_song_from_playlist_playlist_not_found():
    song_name = "song-name"
    file_path = "tests/assets/song.mp3"
    genre = "Pop"
    photo = "https://photo"

    playlist_name = "playlist-name"
    playlist_owner = "playlist-user"
    password = "password"

    res_create_artist = create_artist(playlist_owner, photo, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=playlist_owner, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_remove_song_from_playlist = remove_song_from_playlist(
        name=playlist_name, song_names=[song_name], headers=jwt_headers
    )
    assert res_remove_song_from_playlist.status_code == HTTP_404_NOT_FOUND

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(playlist_owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_remove_song_from_playlist_song_not_found():
    song_name = "song-name"
    photo = "https://photo"

    playlist_name = "playlist-name"
    playlist_owner = "playlist-user"
    description = "playlist-description"
    password = "password"

    res_create_artist = create_artist(playlist_owner, photo, password)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=playlist_owner, password=password)

    res_create_playlist = create_playlist(
        name=playlist_name, descripcion=description, photo=photo, headers=jwt_headers
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_remove_song_from_playlist = remove_song_from_playlist(
        name=playlist_name, song_names=[song_name], headers=jwt_headers
    )
    assert res_remove_song_from_playlist.status_code == HTTP_404_NOT_FOUND

    res_delete_playlist = delete_playlist(playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(playlist_owner)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED
