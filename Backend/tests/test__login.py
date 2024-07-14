import pytest
from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from tests.test_API.api_login import post_login
from tests.test_API.api_test_artist import create_artist
from tests.test_API.api_test_user import create_user, delete_user


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


def test_login_artist(clear_test_data_db):
    password = "hola"
    artista = "artista"
    photo = "https://photo"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    res_login_artist = post_login(artista, password)
    assert res_login_artist.status_code == HTTP_200_OK

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_login_user(clear_test_data_db):
    user_name = "8232392323623823723"
    password = "hola"
    photo = "https://photo"

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    res_login_user = post_login(user_name, password)
    assert res_login_user.status_code == HTTP_200_OK

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_login_user_not_found():
    user_name = "8232392323623823723"
    password = "hola"

    res_login_artist = post_login(user_name, password)
    assert res_login_artist.status_code == HTTP_404_NOT_FOUND


def test_login_user_bad_password(clear_test_data_db):
    user_name = "8232392323623823723"
    password = "hola"
    bad_password = "bad password"
    photo = "https://photo"

    res_create_user = create_user(name=user_name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    res_login_user = post_login(user_name, bad_password)
    assert res_login_user.status_code == HTTP_403_FORBIDDEN

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


# executes after all tests
@pytest.fixture()
def clear_test_data_db():
    user_name = "8232392323623823723"
    artista = "artista"

    delete_user(name=user_name)
    delete_user(name=artista)

    yield
    user_name = "8232392323623823723"
    artista = "artista"

    delete_user(name=user_name)
    delete_user(name=artista)
