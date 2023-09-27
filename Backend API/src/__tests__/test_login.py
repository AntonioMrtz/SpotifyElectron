from test_API.api_login import post_login
from test_API.api_test_artist import create_artist,delete_artist
from test_API.api_test_user import create_user,delete_user
import pytest


def test_login_artist(clear_test_data_db):

    user_name = "8232392323623823723"
    password = "hola"
    artista = "artista"
    foto = "https://foto"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    res_login_artist = post_login(artista,password)
    assert res_login_artist.status_code == 200

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code==202


def test_login_user(clear_test_data_db):

    user_name = "8232392323623823723"
    password = "hola"
    artista = "artista"
    foto = "https://foto"

    res_create_user = create_user(name=user_name,password=password,photo=foto)
    assert res_create_user.status_code == 201

    res_login_user = post_login(user_name,password)
    assert res_login_user.status_code == 200

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code==202

def test_login_user_not_found():

    user_name = "8232392323623823723"
    password = "hola"

    res_login_artist = post_login(user_name,password)
    assert res_login_artist.status_code == 404

def test_login_user_bad_password(clear_test_data_db):

    user_name = "8232392323623823723"
    password = "hola"
    bad_password = "bad password"
    artista = "artista"
    foto = "https://foto"

    res_create_user = create_user(name=user_name,password=password,photo=foto)
    assert res_create_user.status_code == 201

    res_login_user = post_login(user_name,bad_password)
    assert res_login_user.status_code == 401

    res_delete_user = delete_user(user_name)
    assert res_delete_user.status_code==202


# executes after all tests
@pytest.fixture()
def clear_test_data_db():
    user_name = "8232392323623823723"
    artista = "artista"

    delete_user(name=user_name)
    delete_artist(name=artista)

    yield
    user_name = "8232392323623823723"
    artista = "artista"

    delete_user(name=user_name)
    delete_artist(name=artista)
