from datetime import datetime

import pytest
from pytest import fixture
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)

import app.auth.auth_service as auth_service
import app.spotify_electron.user.base_user_service as base_user_service
import app.spotify_electron.user.user.user_service as user_service
from app.auth.auth_schema import VerifyPasswordException
from tests.test_API.api_test_user import create_user, delete_user, get_user
from tests.test_API.api_token import get_user_jwt_header


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


def test_get_user_correct(clear_test_data_db):
    name = "8232392323623823723"
    photo = "https://photo"
    password = "hola"

    formatting = "%Y-%m-%dT%H:%M:%S"
    post_date_iso8601 = datetime.strptime(
        datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), formatting
    )

    res_create_user = create_user(name=name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=name, password=password)

    res_get_user = get_user(name=name, headers=jwt_headers)
    assert res_get_user.status_code == HTTP_200_OK
    assert res_get_user.json()["name"] == name
    assert res_get_user.json()["photo"] == photo

    try:
        fecha = res_get_user.json()["register_date"]
        response_date = datetime.strptime(fecha, formatting)

        assert response_date.hour == post_date_iso8601.hour

    except ValueError:
        assert False

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_get_user_not_found():
    name = "8232392323623823723"

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == HTTP_404_NOT_FOUND


def test_post_user_correct(clear_test_data_db):
    name = "8232392323623823723"
    photo = "https://photo"
    password = "hola"

    res_create_user = create_user(name=name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_delete_user_correct(clear_test_data_db):
    name = "8232392323623823723"
    photo = "https://photo"
    password = "hola"

    res_create_user = create_user(name=name, password=password, photo=photo)
    assert res_create_user.status_code == HTTP_201_CREATED

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == HTTP_202_ACCEPTED


def test_delete_user_not_found(clear_test_data_db):
    name = "8232392323623823723"

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == HTTP_404_NOT_FOUND


def test_delete_user_invalid_name(clear_test_data_db):
    name = ""

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == HTTP_405_METHOD_NOT_ALLOWED


def test_check_encrypted_password_correct():
    name = "8232392323623823723"
    photo = "https://photo"
    password = "hola"
    user_service.create_user(name, photo, password)
    generated_password = base_user_service.get_user_password(name)

    auth_service.verify_password(password, generated_password)
    base_user_service.delete_user(name)


def test_check_encrypted_password_different():
    name = "8232392323623823723"
    photo = "https://photo"
    password = "hola"
    user_service.create_user(name, photo, password)
    password = "hola2"
    generated_password = base_user_service.get_user_password(name)
    with pytest.raises(VerifyPasswordException):
        auth_service.verify_password(password, generated_password)
    base_user_service.delete_user(name)


# executes after all tests
@pytest.fixture()
def clear_test_data_db():
    name = "8232392323623823723"
    delete_user(name=name)

    yield
    name = "8232392323623823723"
    delete_user(name=name)
