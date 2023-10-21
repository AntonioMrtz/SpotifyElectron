from datetime import datetime
from test_API.api_test_playlist import create_playlist, get_playlist, delete_playlist , update_playlist, get_playlists ,get_all_playlists
from test_API.api_test_artist import create_artist,delete_artist
from test_API.api_token import get_user_jwt_header
import json
import pytest


def test_get_playlist_correct(clear_test_data_db):
    name = "8232392323623823723"
    foto = "https://foto"
    descripcion = "hola"
    owner = "usuarioprueba834783478923489734298"
    password = "password"


    formatting = "%Y-%m-%dT%H:%M:%S"
    post_date_iso8601 = datetime.strptime(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),formatting)

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=owner,password=password)

    res_create_playlist = create_playlist(name=name,descripcion=descripcion,foto=foto,headers=jwt_headers)
    assert res_create_playlist.status_code == 201

    res_get_playlist = get_playlist(name=name,headers=jwt_headers)
    assert res_get_playlist.status_code == 200
    assert res_get_playlist.json()["name"]==name
    assert res_get_playlist.json()["photo"]==foto
    assert res_get_playlist.json()["description"]==descripcion
    assert res_get_playlist.json()["owner"]==owner


    try:
        fecha = res_get_playlist.json()["upload_date"]
        response_date = datetime.strptime(fecha, formatting)

        assert response_date.hour==post_date_iso8601.hour

    except ValueError:
        assert False

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == 202

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == 202


def test_get_playlist_not_found():
    name = "8232392323623823723"

    foto = "https://foto"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=owner,password=password)

    res_get_playlist = get_playlist(name=name,headers=jwt_headers)
    assert res_get_playlist.status_code == 404


def test_post_playlist_correct(clear_test_data_db):
    name = "8232392323623823723"
    foto = "https://foto"
    descripcion = "hola"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == 201


    jwt_headers = get_user_jwt_header(username=owner,password=password)

    res_create_playlist = create_playlist(name=name,descripcion=descripcion,foto=foto,headers=jwt_headers)
    assert res_create_playlist.status_code == 201

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == 202

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == 202


def test_delete_playlist_correct(clear_test_data_db):
    name = "8232392323623823723"
    foto = "https://foto"
    descripcion = "hola"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=owner,password=password)

    res_create_playlist = create_playlist(name=name,descripcion=descripcion,foto=foto,headers=jwt_headers)
    assert res_create_playlist.status_code == 201

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == 202

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == 202


def test_delete__playlist_not_found(clear_test_data_db):
    name = "8232392323623823723"

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == 404


def test_delete_playlist_invalid_name(clear_test_data_db):

    name = ""

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == 405


def test_get_playlist_correct():

    name = ""
    artist = "8232392323623823723"
    foto = "https://foto"
    password = "password"

    res_create_artist = create_artist(artist, foto, password)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artist,password=password)

    res_get_playlist = get_playlist(name=name,headers=jwt_headers)
    assert res_get_playlist.status_code == 200

    res_delete_artist = delete_artist(artist)
    assert res_delete_artist.status_code == 202


def test_update_playlist_correct(clear_test_data_db):
    name = "8232392323623823723"
    foto= "foto"
    descripcion = "descripcion"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=owner,password=password)

    res_create_playlist = create_playlist(name=name,descripcion=descripcion,foto=foto,headers=jwt_headers)
    assert res_create_playlist.status_code == 201


    new_description= "nuevadescripcion"

    res_update_playlist = update_playlist(name=name,foto=foto,descripcion=new_description,headers=jwt_headers)
    assert res_update_playlist.status_code == 204

    res_get_playlist = get_playlist(name=name,headers=jwt_headers)
    assert res_get_playlist.status_code == 200
    assert res_get_playlist.json()["description"]==new_description

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == 202

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == 202

def test_update_playlist_correct_nuevo_nombre(clear_test_data_db):
    name = "8232392323623823723"
    foto= "foto"
    descripcion = "descripcion"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=owner,password=password)

    res_create_playlist = create_playlist(name=name,descripcion=descripcion,foto=foto,headers=jwt_headers)
    assert res_create_playlist.status_code == 201

    new_name = "82323923236238237237"
    new_description= "nuevadescripcion"

    res_update_playlist = update_playlist(name=name,foto=foto,descripcion=new_description,nuevo_nombre=new_name,headers=jwt_headers)
    assert res_update_playlist.status_code == 204


    res_get_playlist =get_playlist(new_name,headers=jwt_headers)
    assert res_get_playlist.status_code == 200

    res_delete_playlist = delete_playlist(new_name)
    assert res_delete_playlist.status_code == 202

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == 202



def test_get_playlists(clear_test_data_db):

    foto= "foto"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=owner,password=password)

    res_get_playlists = get_all_playlists(headers=jwt_headers)
    assert res_get_playlists.status_code == 200

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == 202


def test_get_playlists(clear_test_data_db):

    name = "8232392323623823723"
    foto= "foto"
    descripcion = "descripcion"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=owner,password=password)

    res_create_playlist = create_playlist(name=name,descripcion=descripcion,foto=foto,headers=jwt_headers)
    assert res_create_playlist.status_code == 201

    new_name = "82323923236238237237"
    foto= "foto"
    descripcion = "descripcion"

    res_create_playlist = create_playlist(name=new_name,descripcion=descripcion,foto=foto,headers=jwt_headers)
    assert res_create_playlist.status_code == 201

    res_get_playlists = get_playlists(f'{name},{new_name}',headers=jwt_headers)
    assert res_get_playlists.status_code == 200
    assert len(res_get_playlists.json()["playlists"])==2

    res_delete_playlist = delete_playlist(name)
    assert res_delete_playlist.status_code == 202

    res_delete_playlist = delete_playlist(new_name)
    assert res_delete_playlist.status_code == 202

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == 202



# executes after all tests
@pytest.fixture()
def clear_test_data_db():
    new_name = "82323923236238237237"
    name = "8232392323623823723"
    owner = "usuarioprueba834783478923489734298"

    delete_artist(owner)
    delete_playlist(name=name)
    delete_playlist(name=new_name)

    yield
    new_name = "82323923236238237237"
    name = "8232392323623823723"
    owner = "usuarioprueba834783478923489734298"

    delete_artist(owner)
    delete_playlist(name=name)
    delete_playlist(name=new_name)
