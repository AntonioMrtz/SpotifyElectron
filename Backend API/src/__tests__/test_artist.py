from fastapi.testclient import TestClient
from datetime import datetime
from test_API.api_test_artist import create_artist, delete_artist, get_artist, update_artist
from main import app as app
import json
import pytest


def test_get_artist_correct(clear_test_data_db):
    name = "8232392323623823723"
    foto = "https://foto"
    password = "hola"

    formatting = "%Y-%m-%dT%H:%M:%S"
    post_date_iso8601 = datetime.strptime(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),formatting)

    res_create_artist = create_artist(name=name,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    res_get_artist = get_artist(name=name)
    assert res_get_artist.status_code == 200
    assert res_get_artist.json()["name"]==name
    assert res_get_artist.json()["photo"]==foto

    try:
        fecha = res_get_artist.json()["register_date"]
        response_date = datetime.strptime(fecha, formatting)

        assert response_date.hour==post_date_iso8601.hour

    except ValueError:
        assert False

    res_delete_artist = delete_artist(name=name)
    assert res_delete_artist.status_code == 202


def test_get_artist_not_found():
    name = "8232392323623823723"

    res_delete_artist = delete_artist(name=name)
    assert res_delete_artist.status_code == 404


def test_post_artist_correct(clear_test_data_db):
    name = "8232392323623823723"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=name,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    res_delete_artist = delete_artist(name=name)
    assert res_delete_artist.status_code == 202


def test_delete_artist_correct(clear_test_data_db):
    name = "8232392323623823723"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=name,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    res_delete_artist = delete_artist(name=name)
    assert res_delete_artist.status_code == 202


def test_delete_artist_not_found(clear_test_data_db):
    name = "8232392323623823723"

    res_delete_artist = delete_artist(name=name)
    assert res_delete_artist.status_code == 404


def test_delete_artist_invalid_name(clear_test_data_db):

    name = ""

    res_delete_artist = delete_artist(name=name)
    assert res_delete_artist.status_code == 405





def test_update_playlist_correct(clear_test_data_db):

    name = "8232392323623823723"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=name,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    res_update_artist = update_artist(name=name,photo=foto,playlists=["prueba"],saved_playlists=["prueba"],playback_history=["prueba"],uploaded_songs=["prueba"])
    assert res_update_artist.status_code == 204

    res_get_artist = get_artist(name=name)
    assert res_get_artist.status_code == 200
    assert len(res_get_artist.json()["playback_history"])==1
    assert len(res_get_artist.json()["saved_playlists"])==1
    assert len(res_get_artist.json()["playlists"])==1
    assert len(res_get_artist.json()["uploaded_songs"])==1


    res_delete_artist = delete_artist(name=name)
    assert res_delete_artist.status_code == 202



# executes after all tests
@pytest.fixture()
def clear_test_data_db():
    name = "8232392323623823723"
    delete_artist(name=name)

    yield
    name = "8232392323623823723"
    delete_artist(name=name)
