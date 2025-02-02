import os

from pytest import fixture
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_206_PARTIAL_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
)

from tests.test_API.api_stream import stream_song
from tests.test_API.api_test_artist import create_artist
from tests.test_API.api_test_song import create_song, delete_song
from tests.test_API.api_test_user import create_user, delete_user
from tests.test_API.api_token import get_user_jwt_header


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


SONG_PATH = "tests/assets/song_4_seconds.mp3"
SONG_BYTES_SIZE = os.path.getsize(SONG_PATH)


def test_stream_controller_song_invalid_range_no_range_header():
    song_name = "song-name"
    artist_name = "artist-name"
    genre = "Pop"
    photo = "https://photo"
    password = "artist-pass"

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist_name, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=SONG_PATH,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    res_stream_song = stream_song(song_name, jwt_headers)
    assert res_stream_song.status_code == HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_stream_controller_song_invalid_range_greater_than_file_size():
    song_name = "song-name"
    artist_name = "artist-name"
    genre = "Pop"
    photo = "https://photo"
    password = "artist-pass"

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist_name, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=SONG_PATH,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    byte_range_headers = {"Range": f"bytes=0-{SONG_BYTES_SIZE + 10}"}

    res_stream_song = stream_song(song_name, {**jwt_headers, **byte_range_headers})
    assert res_stream_song.status_code == HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_stream_controller_song_invalid_range_start_smaller_end_bytes():
    song_name = "song-name"
    artist_name = "artist-name"
    genre = "Pop"
    photo = "https://photo"
    password = "artist-pass"

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist_name, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=SONG_PATH,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    byte_range_headers = {"Range": f"bytes={SONG_BYTES_SIZE}-0"}

    res_stream_song = stream_song(song_name, {**jwt_headers, **byte_range_headers})
    assert res_stream_song.status_code == HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_stream_controller_song_not_found():
    user_name = "user-name"
    photo = "https://photo"
    password = "user-pass"

    song_name = "song-name"

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=user_name, password=password)

    res_stream_song = stream_song(song_name, jwt_headers)
    assert res_stream_song.status_code == HTTP_404_NOT_FOUND

    res_delete_artist = delete_user(user_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_stream_controller_song_range_correct():
    song_name = "song-name"
    artist_name = "artist-name"
    genre = "Pop"
    photo = "https://photo"
    password = "artist-pass"

    start_requested_bytes = 200
    end_requested_bytes = SONG_BYTES_SIZE - 200

    res_create_artist = create_artist(name=artist_name, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artist_name, password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=SONG_PATH,
        genre=genre,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_song.status_code == HTTP_201_CREATED

    byte_range_headers = {"Range": f"bytes={start_requested_bytes}-{end_requested_bytes}"}

    res_stream_song = stream_song(song_name, {**jwt_headers, **byte_range_headers})
    assert res_stream_song.status_code == HTTP_206_PARTIAL_CONTENT
    assert (
        int(res_stream_song.headers["Content-length"])
        == end_requested_bytes - start_requested_bytes + 1
    )
    assert (
        res_stream_song.headers["Content-range"]
        == f"bytes {start_requested_bytes}-{end_requested_bytes}/{SONG_BYTES_SIZE}"
    )

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == HTTP_202_ACCEPTED

    res_delete_artist = delete_user(artist_name)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED
