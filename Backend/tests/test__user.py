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
from app.spotify_electron.user.user.user_schema import (
    UserAlreadyExistsException,
    UserBadNameException,
    UserBadParametersException,
    UserCreateException,
    UserDAO,
    UserDeleteException,
    UserDTO,
    UserGetPasswordException,
    UserNotFoundException,
    UserRepositoryException,
    UserServiceException,
    UserUpdateException,
    get_user_dao_from_document,
    get_user_dto_from_dao,
)
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


def test_get_user_dao_from_document():
    document = {
        "name": "test_user",
        "photo": "https://photo",
        "register_date": "2024-11-30T12:00:00",
        "password": b"securepassword",
        "playback_history": ["song1", "song2"],
        "playlists": ["playlist1", "playlist2"],
        "saved_playlists": ["saved_playlist1"],
    }

    user_dao = get_user_dao_from_document(document)

    assert isinstance(user_dao, UserDAO)
    assert user_dao.name == "test_user"
    assert user_dao.photo == "https://photo"
    assert user_dao.register_date == "2024-11-30T12:00:00"
    assert user_dao.password == b"securepassword"
    assert user_dao.playback_history == ["song1", "song2"]
    assert user_dao.playlists == ["playlist1", "playlist2"]
    assert user_dao.saved_playlists == ["saved_playlist1"]


def test_get_user_dto_from_dao():
    user_dao = UserDAO(
        name="test_user",
        photo="https://photo",
        register_date="2024-11-30T12:00:00",
        password=b"securepassword",
        playback_history=["song1", "song2"],
        playlists=["playlist1", "playlist2"],
        saved_playlists=["saved_playlist1"],
    )

    user_dto = get_user_dto_from_dao(user_dao)

    assert isinstance(user_dto, UserDTO)
    assert user_dto.name == "test_user"
    assert user_dto.photo == "https://photo"
    assert user_dto.register_date == "2024-11-30T12:00:00"
    assert user_dto.playback_history == ["song1", "song2"]
    assert user_dto.playlists == ["playlist1", "playlist2"]
    assert user_dto.saved_playlists == ["saved_playlist1"]


def test_user_repository_exception():
    with pytest.raises(UserRepositoryException) as exc_info:
        raise UserRepositoryException()
    assert str(exc_info.value) == UserRepositoryException.ERROR


def test_user_not_found_exception():
    with pytest.raises(UserNotFoundException) as exc_info:
        raise UserNotFoundException()
    assert str(exc_info.value) == UserNotFoundException.ERROR


def test_user_already_exists_exception():
    with pytest.raises(UserAlreadyExistsException) as exc_info:
        raise UserAlreadyExistsException()
    assert str(exc_info.value) == UserAlreadyExistsException.ERROR


def test_user_bad_name_exception():
    with pytest.raises(UserBadNameException) as exc_info:
        raise UserBadNameException()
    assert str(exc_info.value) == UserBadNameException.ERROR


def test_user_create_exception():
    with pytest.raises(UserCreateException) as exc_info:
        raise UserCreateException()
    assert str(exc_info.value) == UserCreateException.ERROR


def test_user_delete_exception():
    with pytest.raises(UserDeleteException) as exc_info:
        raise UserDeleteException()
    assert str(exc_info.value) == UserDeleteException.ERROR


def test_user_update_exception():
    with pytest.raises(UserUpdateException) as exc_info:
        raise UserUpdateException()
    assert str(exc_info.value) == UserUpdateException.ERROR


def test_user_bad_parameters_exception():
    with pytest.raises(UserBadParametersException) as exc_info:
        raise UserBadParametersException()
    assert str(exc_info.value) == UserBadParametersException.ERROR


def test_user_get_password_exception():
    with pytest.raises(UserGetPasswordException) as exc_info:
        raise UserGetPasswordException()
    assert str(exc_info.value) == UserGetPasswordException.ERROR


def test_user_service_exception():
    with pytest.raises(UserServiceException) as exc_info:
        raise UserServiceException()
    assert str(exc_info.value) == UserServiceException.ERROR


# executes after all tests
@pytest.fixture()
def clear_test_data_db():
    name = "8232392323623823723"
    delete_user(name=name)

    yield
    name = "8232392323623823723"
    delete_user(name=name)
