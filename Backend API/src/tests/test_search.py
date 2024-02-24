from test_API.api_test_search import get_search_by_name
from test_API.api_test_user import create_user,delete_user
from test_API.api_token import get_user_jwt_header
from test_API.api_test_playlist import create_playlist,delete_playlist
import pytest
import json


def test_get_search_by_name_correct(clear_test_data_db):
    name = "8232392323623823723"
    foto = "https://foto"
    descripcion = "hola"
    password = "password"
    playlist_name = "playlist"

    res_create_user = create_user(name,foto,password)
    assert res_create_user.status_code == 201

    jwt_headers = get_user_jwt_header(username=name,password=password)

    res_create_playlist = create_playlist(name=playlist_name,descripcion=descripcion,foto=foto,headers=jwt_headers)
    assert res_create_playlist.status_code == 201

    res_search_by_name = get_search_by_name("playlist",jwt_headers)
    assert res_search_by_name.status_code == 200
    json.loads(res_search_by_name.json()["playlists"][0])["name"]==playlist_name

    res_delete_playlist = delete_playlist(name=playlist_name)
    assert res_delete_playlist.status_code == 202

    res_delete_user = delete_user(name)
    assert res_delete_user.status_code == 202


def test_get_search_by_name_invalid_name(clear_test_data_db):
    name = "8232392323623823723"
    foto = "https://foto"
    descripcion = "hola"
    password = "password"
    playlist_name = "playlist"

    res_create_user = create_user(name,foto,password)
    assert res_create_user.status_code == 201

    jwt_headers = get_user_jwt_header(username=name,password=password)

    res_search_by_name = get_search_by_name("",jwt_headers)
    assert res_search_by_name.status_code == 400

    res_delete_user = delete_user(name)
    assert res_delete_user.status_code == 202


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
