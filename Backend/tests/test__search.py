import pytest
from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
)

from tests.test_API.api_test_playlist import create_playlist, delete_playlist
from tests.test_API.api_test_search import get_search_by_name
from tests.test_API.api_test_user import create_user, delete_user
from tests.test_API.api_token import get_user_jwt_header


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


def test_get_search_by_name_correct(clear_test_data_db):
    # TODO, crear los demas items y comprobarlos
    name = "8232392323623823723"
    photo = "https://photo"
    descripcion = "hola"
    password = "password"
    playlist_name = "playlist"

    res_create_user = create_user(name, photo, password)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=name, password=password)

    res_create_playlist = create_playlist(
        name=playlist_name,
        descripcion=descripcion,
        photo=photo,
        headers=jwt_headers,
    )
    assert res_create_playlist.status_code == HTTP_201_CREATED

    res_search_by_name = get_search_by_name("playlist", jwt_headers)
    assert res_search_by_name.status_code == HTTP_200_OK
    assert res_search_by_name.json()["playlists"][0]["name"] == playlist_name

    res_delete_playlist = delete_playlist(name=playlist_name)
    assert res_delete_playlist.status_code == HTTP_202_ACCEPTED

    res_delete_user = delete_user(name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_get_search_by_name_invalid_name(clear_test_data_db):
    name = "8232392323623823723"
    photo = "https://photo"
    password = "password"

    res_create_user = create_user(name, photo, password)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=name, password=password)

    res_search_by_name = get_search_by_name("", jwt_headers)
    assert res_search_by_name.status_code == HTTP_400_BAD_REQUEST

    res_delete_user = delete_user(name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


# executes after all tests
@pytest.fixture()
def clear_test_data_db():
    name = "8232392323623823723"
    playlist_name = "playlist"

    delete_user(name)
    delete_playlist(playlist_name)

    yield
    name = "8232392323623823723"
    playlist_name = "playlist"

    delete_user(name)
    delete_playlist(playlist_name)
