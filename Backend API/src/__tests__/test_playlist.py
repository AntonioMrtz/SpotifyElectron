from fastapi.testclient import TestClient
from datetime import datetime
from test_API.api_test_playlist import create_playlist, get_playlist, delete_playlist , update_playlist
from main import app as app
import json
import pytest

client = TestClient(app)


def test_get_playlist_correct(clear_test_data_db):
    name = "8232392323623823723"
    foto = "https://foto"
    descripcion = "hola"

    formatting = "%Y-%m-%dT%H:%M:%S"
    post_date_iso8601 = datetime.strptime(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),formatting)

    url = f"/playlists/?nombre={name}&foto={foto}&descripcion={descripcion}"

    res_create_playlist = create_playlist(name=name,descripcion=descripcion,foto=foto)
    assert res_create_playlist.status_code == 201

    res_get_playlist = get_playlist(name=name)
    assert res_get_playlist.status_code == 200
    assert res_get_playlist.json()["name"]==name
    assert res_get_playlist.json()["photo"]==foto
    assert res_get_playlist.json()["description"]==descripcion

    try:
        fecha = res_get_playlist.json()["upload_date"]
        response_date = datetime.strptime(fecha, formatting)

        assert response_date.hour==post_date_iso8601.hour

    except ValueError:
        assert False

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == 202


def test_get_playlist_not_found():
    name = "8232392323623823723"

    res_get_playlist = get_playlist(name=name)
    assert res_get_playlist.status_code == 404


def test_post_playlist_correct(clear_test_data_db):
    name = "8232392323623823723"
    foto = "https://foto"
    descripcion = "hola"

    res_create_playlist = create_playlist(name=name,descripcion=descripcion,foto=foto)
    assert res_create_playlist.status_code == 201

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == 202


def test_delete_playlist_correct(clear_test_data_db):
    name = "8232392323623823723"
    foto = "https://foto"
    descripcion = "hola"

    res_create_playlist = create_playlist(name=name,descripcion=descripcion,foto=foto)
    assert res_create_playlist.status_code == 201

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == 202


def test_delete_playlist_playlist_not_found(clear_test_data_db):
    name = "8232392323623823723"

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == 404


def test_delete_playlist_playlist_invalid_name(clear_test_data_db):
    """Cannot recreate error 404 because name cant be empty or None to reach the actual python method"""

    name = ""

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == 405


def test_get_playlists_correct():
    name = ""

    res_get_playlist = get_playlist(name=name)
    assert res_get_playlist.status_code == 200


def test_update_playlist_correct(clear_test_data_db):
    name = "8232392323623823723"
    foto= "foto"
    descripcion = "descripcion"

    res_create_playlist = create_playlist(name=name,descripcion=descripcion,foto=foto)
    assert res_create_playlist.status_code == 201

    new_description= "nuevadescripcion"

    res_update_playlist = update_playlist(name=name,foto=foto,descripcion=new_description)
    assert res_update_playlist.status_code == 204

    res_get_playlist = get_playlist(name=name)
    assert res_get_playlist.status_code == 200
    assert res_get_playlist.json()["description"]==new_description

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == 202

def test_update_playlist_correct_nuevo_nombre(clear_test_data_db):
    name = "8232392323623823723"
    foto= "foto"
    descripcion = "descripcion"

    res_create_playlist = create_playlist(name=name,descripcion=descripcion,foto=foto)
    assert res_create_playlist.status_code == 201

    new_name = "82323923236238237237"
    new_description= "nuevadescripcion"

    res_update_playlist = update_playlist(name=name,foto=foto,descripcion=new_description,nuevo_nombre=new_name)
    assert res_update_playlist.status_code == 204


    res_get_playlist =get_playlist(new_name)
    assert res_get_playlist.status_code == 200

    res_delete_playlist = delete_playlist(new_name)
    assert res_delete_playlist.status_code == 202


# executes after all tests
@pytest.fixture()
def clear_test_data_db():
    new_name = "82323923236238237237"
    name = "8232392323623823723"
    response = client.delete(f"/playlists/{new_name}")
    response = client.delete(f"/playlists/{name}")

    yield
    new_name = "82323923236238237237"
    name = "8232392323623823723"
    response = client.delete(f"/playlists/{new_name}")
    response = client.delete(f"/playlists/{name}")
