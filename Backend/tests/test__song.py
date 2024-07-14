import pytest
from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from app.spotify_electron.genre.genre_schema import Genre
from tests.test_API.api_test_artist import create_artist, get_artist
from tests.test_API.api_test_song import (
    create_song,
    delete_song,
    get_song,
    get_songs_by_genre,
    increase_song_streams,
)
from tests.test_API.api_test_user import create_user, delete_user
from tests.test_API.api_token import get_user_jwt_header


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


def test_post_cancion_correct(clear_test_data_db):
    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genre = "Pop"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_post_cancion_user_as_artist(clear_test_data_db):
    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    username = "artista"
    genre = "Pop"
    photo = "https://photo"
    password = "hola"

    res_create_user = create_user(name=username, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=username, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_403_FORBIDDEN


def test_post_cancion_correct_check_valid_duration(clear_test_data_db):
    song_name = "8232392323623823723989"
    file_path = "tests/assets/song_4_seconds.mp3"
    artista = "artista"
    genre = "Pop"

    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_get_song = get_song(name=song_name, headers=jwt_headers)
    assert res_get_song.status_code == HTTP_200_OK
    assert str(res_get_song.json()["seconds_duration"]).split(".")[0] == "4"

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_post_cancion_correct_check_invalid_duration(clear_test_data_db):
    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genre = "Pop"

    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_get_song = get_song(name=song_name, headers=jwt_headers)
    assert res_get_song.status_code == HTTP_200_OK
    assert "0" in str(res_get_song.json()["seconds_duration"])

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_cancion_correct(clear_test_data_db):
    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genre = "Pop"
    photo = "https://photo"

    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_get_song = get_song(name=song_name, headers=jwt_headers)
    assert res_get_song.status_code == HTTP_200_OK
    assert res_get_song.json()["name"] == song_name
    assert res_get_song.json()["artist"] == artista
    assert res_get_song.json()["genre"] == Genre(genre)
    assert res_get_song.json()["photo"] == photo

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_cancion_invalid_name(clear_test_data_db):
    artista = "artista"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    song_name = "8232392323623823723989"

    res_get_song = get_song(name=song_name, headers=jwt_headers)
    assert res_get_song.status_code == HTTP_404_NOT_FOUND

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_delete_cancion_correct(clear_test_data_db):
    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genre = "Pop"
    photo = "https://photo"

    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_delete_cancion_not_found():
    song_name = "8232392323623823723989"

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_404_NOT_FOUND


def test_patch_number_plays_cancion_correct(clear_test_data_db):
    song_name = "8232392323623823723989"
    artista = "artista"
    genre = "Pop"
    photo = "https://photo"
    file_path = "tests/assets/song.mp3"

    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_increase_streams_song = increase_song_streams(name=song_name, headers=jwt_headers)
    assert res_increase_streams_song.status_code == HTTP_204_NO_CONTENT

    res_get_song = get_song(name=song_name, headers=jwt_headers)
    assert res_get_song.status_code == HTTP_200_OK
    assert res_get_song.json()["name"] == song_name
    assert res_get_song.json()["artist"] == artista
    assert res_get_song.json()["genre"] == Genre(genre)
    assert res_get_song.json()["photo"] == photo
    assert res_get_song.json()["streams"] == 1

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_patch_number_of_plays_song_not_found(clear_test_data_db):
    song_name = "8232392323623823723989"
    artista = "artista"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    song_name = "8232392323623823723989"

    res_increase_streams_song = increase_song_streams(name=song_name, headers=jwt_headers)
    assert res_increase_streams_song.status_code == HTTP_404_NOT_FOUND


def test_patch_song_invalid_name(clear_test_data_db):
    song_name = "8232392323623823723989"
    artista = "artista"
    photo = "https://photo"

    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    song_name = ""

    res_increase_streams_song = increase_song_streams(name=song_name, headers=jwt_headers)
    assert res_increase_streams_song.status_code == HTTP_404_NOT_FOUND


def test_post_song_uploaded_songs_updated(clear_test_data_db):
    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genre = "Pop"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_get_artist = get_artist(name=artista, headers=jwt_headers)
    assert res_get_artist.status_code == HTTP_200_OK
    assert len(res_get_artist.json()["uploaded_songs"]) == 1
    assert res_get_artist.json()["uploaded_songs"][0] == song_name

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_post_song_uploaded_songs_bad_artist(clear_test_data_db):
    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genre = "Pop"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_404_NOT_FOUND


def test_delete_song_uploaded_songs_updated(clear_test_data_db):
    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genre = "Pop"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_get_artist = get_artist(name=artista, headers=jwt_headers)
    assert res_get_artist.status_code == HTTP_200_OK
    assert len(res_get_artist.json()["uploaded_songs"]) == 0

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_cancion_by_genre(clear_test_data_db):
    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genre = "Rock"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_get_song_by_genre = get_songs_by_genre(genre=genre, headers=jwt_headers)
    assert res_get_song_by_genre.status_code == HTTP_200_OK
    assert len(res_get_song_by_genre.json()) == 1

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_cancion_by_genre_bad_genre(clear_test_data_db):
    genre = "RockInventado"

    artista = "artista"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    res_get_song_by_genre = get_songs_by_genre(genre=genre, headers=jwt_headers)
    assert res_get_song_by_genre.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


@pytest.fixture()
def clear_test_data_db():
    song_name = "8232392323623823723989"
    artista = "artista"
    delete_song(song_name)
    delete_user(artista)
    delete_user(artista)

    yield
    song_name = "8232392323623823723989"
    artista = "artista"
    delete_song(song_name)
    delete_user(artista)
    delete_user(artista)
