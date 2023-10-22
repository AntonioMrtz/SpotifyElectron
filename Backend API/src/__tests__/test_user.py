from datetime import datetime
from test_API.api_test_user import create_user, delete_user, get_user, update_user
from test_API.api_token import get_user_jwt_header
import json
import pytest
import bcrypt


def test_get_user_correct(clear_test_data_db):
    name = "8232392323623823723"
    foto = "https://foto"
    password = "hola"

    formatting = "%Y-%m-%dT%H:%M:%S"
    post_date_iso8601 = datetime.strptime(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),formatting)

    res_create_user = create_user(name=name,password=password,photo=foto)
    assert res_create_user.status_code == 201

    jwt_headers = get_user_jwt_header(username=name,password=password)

    res_get_user = get_user(name=name,headers=jwt_headers)
    assert res_get_user.status_code == 200
    assert res_get_user.json()["name"]==name
    assert res_get_user.json()["photo"]==foto

    # check password

    utf8_password = res_get_user.json()["password"].encode('utf-8')
    assert bcrypt.checkpw(password.encode('utf-8'),utf8_password)==True

    try:
        fecha = res_get_user.json()["register_date"]
        response_date = datetime.strptime(fecha, formatting)

        assert response_date.hour==post_date_iso8601.hour

    except ValueError:
        assert False

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == 202


def test_get_user_not_found():
    name = "8232392323623823723"

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == 404


def test_post_user_correct(clear_test_data_db):
    name = "8232392323623823723"
    foto = "https://foto"
    password = "hola"

    res_create_user = create_user(name=name,password=password,photo=foto)
    assert res_create_user.status_code == 201

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == 202


def test_delete_user_correct(clear_test_data_db):
    name = "8232392323623823723"
    foto = "https://foto"
    password = "hola"

    res_create_user = create_user(name=name,password=password,photo=foto)
    assert res_create_user.status_code == 201

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == 202


def test_delete_user_not_found(clear_test_data_db):
    name = "8232392323623823723"

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == 404


def test_delete_user_invalid_name(clear_test_data_db):
    name = ""

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == 405


def test_update_playlists_correct(clear_test_data_db):

    name = "8232392323623823723"
    foto = "https://foto"
    password = "hola"

    res_create_user = create_user(name=name,password=password,photo=foto)
    assert res_create_user.status_code == 201

    jwt_headers = get_user_jwt_header(username=name,password=password)

    res_update_user = update_user(name=name,photo=foto,playlists=["prueba"],saved_playlists=["prueba"],playback_history=["prueba"],headers=jwt_headers)
    assert res_update_user.status_code == 204

    res_get_user = get_user(name=name,headers=jwt_headers)
    assert res_get_user.status_code == 200
    assert len(res_get_user.json()["playback_history"])==1
    assert len(res_get_user.json()["saved_playlists"])==1
    assert len(res_get_user.json()["playlists"])==1

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == 202


# executes after all tests
@pytest.fixture()
def clear_test_data_db():
    name = "8232392323623823723"
    delete_user(name=name)

    yield
    name = "8232392323623823723"
    delete_user(name=name)
