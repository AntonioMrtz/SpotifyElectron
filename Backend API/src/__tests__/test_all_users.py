from main import app as app
from test_API.api_test_user import create_user, delete_user, get_user
from test_API.api_test_artist import create_artist, delete_artist, get_artist
from test_API.api_all_users import patch_history_playback
from test_API.api_test_song import create_song,delete_song
import json
import pytest

def test_patch_playback_history_user_correct(clear_test_data_db):

    name = "8232392323623823723"
    foto = "https://foto"
    password = "hola"

    res_create_user = create_user(name=name,password=password,photo=foto)
    assert res_create_user.status_code == 201

    song_name = "8232392323623823723989"
    file_path = "__tests__/assets/song.mp3"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"

    res_create_song = create_song(name=song_name,file_path=file_path,artista=artista,genero=genero,foto=foto)
    assert res_create_song.status_code == 201

    res_patch_user = patch_history_playback(name,song_name)
    assert res_patch_user.status_code == 204


    res_get_user = get_user(name=name)
    assert res_get_user.status_code == 200
    assert len(res_get_user.json()["playback_history"])==1
    assert res_get_user.json()["playback_history"][0]==song_name

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == 202

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202

def test_patch_playback_history_artist_correct(clear_test_data_db):

    name = "8232392323623823723"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=name,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    song_name = "8232392323623823723989"
    file_path = "__tests__/assets/song.mp3"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"

    res_create_song = create_song(name=song_name,file_path=file_path,artista=artista,genero=genero,foto=foto)
    assert res_create_song.status_code == 201

    res_patch_user = patch_history_playback(name,song_name)
    assert res_patch_user.status_code == 204


    res_get_artist = get_artist(name=name)
    assert res_get_artist.status_code == 200
    assert len(res_get_artist.json()["playback_history"])==1
    assert res_get_artist.json()["playback_history"][0]==song_name

    res_delete_artist = delete_artist(name=name)
    assert res_delete_artist.status_code == 202

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202

def test_patch_playback_history_invalid_bad_user():

    res_patch_user = patch_history_playback("","")
    assert res_patch_user.status_code == 404

def test_patch_playback_history_non_existing_user():

    res_patch_user = patch_history_playback("usuario1","cancion1")
    assert res_patch_user.status_code == 404


def test_patch_playback_history_user_correct_insert_6_songs(clear_test_data_db):

    name = "8232392323623823723"
    foto = "https://foto"
    password = "hola"

    res_create_user = create_user(name=name,password=password,photo=foto)
    assert res_create_user.status_code == 201

    song_name = "8232392323623823723989"
    file_path = "__tests__/assets/song.mp3"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"


    new_song_name = "cancionnueva"


    res_create_song = create_song(name=song_name,file_path=file_path,artista=artista,genero=genero,foto=foto)
    assert res_create_song.status_code == 201

    res_create_song = create_song(name=new_song_name,file_path=file_path,artista=artista,genero=genero,foto=foto)
    assert res_create_song.status_code == 201

    res_patch_user = patch_history_playback(name,song_name)
    assert res_patch_user.status_code == 204

    res_patch_user = patch_history_playback(name,song_name)
    assert res_patch_user.status_code == 204

    res_patch_user = patch_history_playback(name,song_name)
    assert res_patch_user.status_code == 204

    res_patch_user = patch_history_playback(name,song_name)
    assert res_patch_user.status_code == 204

    res_patch_user = patch_history_playback(name,song_name)
    assert res_patch_user.status_code == 204

    res_patch_user = patch_history_playback(name,new_song_name)
    assert res_patch_user.status_code == 204


    res_get_user = get_user(name=name)
    assert res_get_user.status_code == 200
    assert len(res_get_user.json()["playback_history"])==5
    assert res_get_user.json()["playback_history"][4]==new_song_name

    res_delete_user = delete_user(name=name)
    assert res_delete_user.status_code == 202

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202

    res_delete_song = delete_song(new_song_name)
    assert res_delete_song.status_code == 202




# executes after all tests
@pytest.fixture()
def clear_test_data_db():
    name = "8232392323623823723"
    song_name = "8232392323623823723989"
    new_song_name = "cancionnueva"

    delete_user(name=name)
    delete_song(name=song_name)
    delete_song(name=new_song_name)


    yield
    name = "8232392323623823723"
    song_name = "8232392323623823723989"
    new_song_name = "cancionnueva"

    delete_user(name=name)
    delete_artist(name=name)
    delete_song(name=song_name)
    delete_song(name=new_song_name)
