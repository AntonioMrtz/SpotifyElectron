from datetime import datetime
from test_API.api_test_artist import create_artist, delete_artist, get_artist, update_artist, get_artists, get_play_count_artist
from test_API.api_test_song import create_song, delete_song, patch_song_number_plays
from test_API.api_token import get_user_jwt_header
import bcrypt
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

    jwt_headers = get_user_jwt_header(username=name,password=password)

    res_get_artist = get_artist(name=name,headers=jwt_headers)
    assert res_get_artist.status_code == 200
    assert res_get_artist.json()["name"]==name
    assert res_get_artist.json()["photo"]==foto

    # check password

    utf8_password = res_get_artist.json()["password"].encode('utf-8')
    assert bcrypt.checkpw(password.encode('utf-8'),utf8_password)==True


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


def test_get_artists_correct():

    name = "8232392323623823723"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=name,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=name,password=password)

    res_get_artists = get_artists(headers=jwt_headers)
    assert res_get_artists.status_code==200

    res_delete_artist = delete_artist(name=name)
    assert res_delete_artist.status_code == 202


def test_update_playlists_correct(clear_test_data_db):

    name = "8232392323623823723"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=name,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=name,password=password)

    res_update_artist = update_artist(name=name,photo=foto,playlists=["prueba"],saved_playlists=["prueba"],playback_history=["prueba"],uploaded_songs=["prueba"],headers=jwt_headers)
    assert res_update_artist.status_code == 204

    res_get_artist = get_artist(name=name,headers=jwt_headers)
    assert res_get_artist.status_code == 200
    assert len(res_get_artist.json()["playback_history"])==1
    assert len(res_get_artist.json()["saved_playlists"])==1
    assert len(res_get_artist.json()["playlists"])==1
    assert len(res_get_artist.json()["uploaded_songs"])==1


    res_delete_artist = delete_artist(name=name)
    assert res_delete_artist.status_code == 202

def test_get_play_count_artist_correct(clear_test_data_db):

    song_name = "8232392323623823723989"
    song_name_2 = "82323923236238237239892"
    file_path = "tests/assets/song.mp3"
    artista = "8232392323623823723"
    genero = "Pop"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)

    res_create_song = create_song(name=song_name,file_path=file_path,genero=genero,foto=foto,headers=jwt_headers)
    assert res_create_song.status_code == 201

    res_create_song = create_song(name=song_name_2,file_path=file_path,genero=genero,foto=foto,headers=jwt_headers)
    assert res_create_song.status_code == 201

    res_patch_song = patch_song_number_plays(name=song_name,headers=jwt_headers)
    assert res_patch_song.status_code==204

    res_patch_song = patch_song_number_plays(name=song_name_2,headers=jwt_headers)
    assert res_patch_song.status_code==204

    res_get_play_count_artist = get_play_count_artist(artista,headers=jwt_headers)
    assert res_get_play_count_artist.status_code == 200
    assert res_get_play_count_artist.json()["play_count"]==2


    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202

    res_delete_song = delete_song(song_name_2)
    assert res_delete_song.status_code == 202

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202



# executes after all tests
@pytest.fixture()
def clear_test_data_db():
    name = "8232392323623823723"
    delete_artist(name=name)

    yield
    name = "8232392323623823723"
    delete_artist(name=name)
