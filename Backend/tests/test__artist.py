from datetime import datetime

from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)
from test_API.api_test_artist import (
    create_artist,
    get_artist,
    get_artist_songs,
    get_artists,
)

from tests.test_API.api_test_song import create_song, delete_song, increase_song_streams
from tests.test_API.api_test_user import create_user, delete_user
from tests.test_API.api_token import get_user_jwt_header


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


def test_get_artist_correct(clear_test_data_db):
    name = "8232392323623823723"
    photo = "https://photo"
    password = "hola"

    formatting = "%Y-%m-%dT%H:%M:%S"
    post_date_iso8601 = datetime.strptime(
        datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), formatting
    )

    res_create_artist = create_artist(name=name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=name, password=password)

    res_get_artist = get_artist(name=name, headers=jwt_headers)
    assert res_get_artist.status_code == HTTP_200_OK
    assert res_get_artist.json()["name"] == name
    assert res_get_artist.json()["photo"] == photo

    try:
        fecha = res_get_artist.json()["register_date"]
        response_date = datetime.strptime(fecha, formatting)

        assert response_date.hour == post_date_iso8601.hour

    except ValueError:
        assert False

    res_delete_artist = delete_user(name=name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_artist_not_found():
    name = "8232392323623823723"
    photo = "https://photo"
    password = "hola"

    non_existent_artist = "non_existent_artist"

    res_create_artist = create_artist(name=name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=name, password=password)

    res_get_artist = get_artist(name=non_existent_artist, headers=jwt_headers)
    assert res_get_artist.status_code == HTTP_404_NOT_FOUND

    res_delete_artist = delete_user(name=name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_post_artist_correct(clear_test_data_db):
    name = "8232392323623823723"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    res_delete_artist = delete_user(name=name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_post_artist_already_exists(clear_test_data_db):
    name = "8232392323623823723"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    res_create_artist = create_artist(name=name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_400_BAD_REQUEST

    res_delete_artist = delete_user(name=name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_delete_artist_correct(clear_test_data_db):
    name = "8232392323623823723"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    res_delete_artist = delete_user(name=name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_delete_artist_not_found(clear_test_data_db):
    name = "8232392323623823723"

    res_delete_artist = delete_user(name=name)
    assert res_delete_artist.status_code == HTTP_404_NOT_FOUND


def test_delete_artist_invalid_name(clear_test_data_db):
    name = ""

    res_delete_artist = delete_user(name=name)
    assert res_delete_artist.status_code == HTTP_405_METHOD_NOT_ALLOWED


def test_get_artists_correct():
    name = "8232392323623823723"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=name, password=password)

    res_get_artists = get_artists(headers=jwt_headers)
    assert res_get_artists.status_code == HTTP_200_OK

    res_delete_artist = delete_user(name=name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_total_streams_artist_correct(clear_test_data_db):
    song_name_1 = "8232392323623823723989"
    song_name_2 = "82323923236238237239892"
    file_path = "tests/assets/song.mp3"
    artist_name = "8232392323623823723"
    genre = "Pop"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist_name, password=password)

    res_create_song_1 = create_song(
        name=song_name_1,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song_1.status_code == HTTP_201_CREATED

    res_create_song_2 = create_song(
        name=song_name_2,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song_2.status_code == HTTP_201_CREATED

    increase_song_streams(name=song_name_1, headers=jwt_headers)
    increase_song_streams(name=song_name_2, headers=jwt_headers)

    res_get_artist = get_artist(name=artist_name, headers=jwt_headers)
    assert res_get_artist.status_code == HTTP_200_OK

    artist_data = res_get_artist.json()
    expected_total_streams = 2
    assert "total_streams" in artist_data
    assert artist_data["total_streams"] == expected_total_streams

    res_delete_song_1 = delete_song(song_name_1)
    assert res_delete_song_1.status_code == HTTP_202_ACCEPTED

    res_delete_song_2 = delete_song(song_name_2)
    assert res_delete_song_2.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_artist_songs_correct():
    song_name = "8232392323623823723989"
    song_name_2 = "82323923236238237239892"
    file_path = "tests/assets/song.mp3"
    artist = "8232392323623823723"
    genre = "Pop"
    photo = "https://photo"
    password = "hola"
    exptected_artists_songs = [song_name, song_name_2]

    res_create_artist = create_artist(name=artist, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_create_song = create_song(
        name=song_name_2,
        file_path=file_path,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_get_artists_songs = get_artist_songs(artist, jwt_headers)
    assert res_get_artists_songs.status_code == HTTP_200_OK
    assert set(exptected_artists_songs) == set(
        [song["name"] for song in res_get_artists_songs.json()]
    )

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_song = delete_song(song_name_2)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_get_artist_songs_user_unauthorized():
    user_name = "8232392323623823723"
    photo = "https://photo"
    password = "hola"

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=user_name, password=password)

    res_get_artists_songs = get_artist_songs(user_name, jwt_headers)
    assert res_get_artists_songs.status_code == HTTP_403_FORBIDDEN

    res_delete_artist = delete_user(user_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


# executes after all tests
@fixture()
def clear_test_data_db():
    name = "8232392323623823723"
    delete_user(name=name)

    yield
    name = "8232392323623823723"
    delete_user(name=name)
