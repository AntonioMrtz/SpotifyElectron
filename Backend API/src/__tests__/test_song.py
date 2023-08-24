from fastapi.testclient import TestClient
from fastapi import UploadFile
from model.Genre import Genre
import io
from test_API.api_test_song import create_song,delete_song,get_song,get_songs,patch_song_number_plays
import json
import pytest

from main import app as app


client = TestClient(app)


def test_post_cancion_correct(clear_test_data_db):

    song_name = "8232392323623823723989"
    file_path = "__tests__/assets/song.mp3"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"

    res_create_song = create_song(name=song_name,file_path=file_path,artista=artista,genero=genero,foto=foto)
    assert res_create_song.status_code == 201

    res_delete_song = delete_song(name=song_name)
    assert res_delete_song.status_code == 202



def test_post_cancion_correct_check_valid_duration(clear_test_data_db):

    song_name = "8232392323623823723989"
    file_path = "__tests__/assets/song_4_seconds.mp3"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"

    res_create_song = create_song(name=song_name,file_path=file_path,artista=artista,genero=genero,foto=foto)
    assert res_create_song.status_code == 201

    res_get_song = get_song(name=song_name)
    assert res_get_song.status_code == 200
    assert "4" == str(res_get_song.json()["duration"]).split(".")[0]

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202


def test_post_cancion_correct_check_invalid_duration(clear_test_data_db):


    song_name = "8232392323623823723989"
    file_path = "__tests__/assets/song.mp3"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"

    res_create_song = create_song(name=song_name,file_path=file_path,artista=artista,genero=genero,foto=foto)
    assert res_create_song.status_code == 201

    res_get_song = get_song(name=song_name)
    assert res_get_song.status_code == 200
    assert "0" in str(res_get_song.json()["duration"])

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202




def test_get_cancion_correct(clear_test_data_db):

    song_name = "8232392323623823723989"
    file_path = "__tests__/assets/song.mp3"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"

    res_create_song = create_song(name=song_name,file_path=file_path,artista=artista,genero=genero,foto=foto)
    assert res_create_song.status_code == 201

    res_get_song = get_song(name=song_name)
    assert res_get_song.status_code == 200
    assert res_get_song.json()["name"]==song_name
    assert res_get_song.json()["artist"]==artista
    assert res_get_song.json()["genre"]==Genre(genero).name
    assert res_get_song.json()["photo"]==foto

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202



def test_get_cancion_invalid_name():

    song_name = "8232392323623823723989"

    res_get_song = get_song(name=song_name)
    assert res_get_song.status_code == 404



def test_delete_cancion_correct():

    song_name = "8232392323623823723989"
    file_path = "__tests__/assets/song.mp3"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"

    res_create_song = create_song(name=song_name,file_path=file_path,artista=artista,genero=genero,foto=foto)
    assert res_create_song.status_code == 201

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202


def test_delete_cancion_not_found():

    song_name = "8232392323623823723989"

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 404


def test_get_canciones_correct():
    res_get_songs = get_songs()
    assert res_get_songs.status_code == 200


def test_patch_number_plays_cancion_correct(clear_test_data_db):

    song_name = "8232392323623823723989"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"
    file_path = "__tests__/assets/song.mp3"


    res_create_song = create_song(name=song_name,file_path=file_path,artista=artista,genero=genero,foto=foto)
    assert res_create_song.status_code == 201

    res_patch_song = patch_song_number_plays(name=song_name)
    assert res_patch_song.status_code==204

    res_get_song = get_song(name=song_name)
    assert res_get_song.status_code == 200
    assert res_get_song.json()["name"]==song_name
    assert res_get_song.json()["artist"]==artista
    assert res_get_song.json()["genre"]==Genre(genero).name
    assert res_get_song.json()["photo"]==foto
    assert res_get_song.json()["number_of_plays"]==1

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202


def test_patch_song_not_found():

    song_name = "8232392323623823723989"

    res_patch_song = patch_song_number_plays(name=song_name)
    assert res_patch_song.status_code==404


def test_patch_song_invalid_name():

    song_name = ""

    res_patch_song = patch_song_number_plays(name=song_name)
    assert res_patch_song.status_code==404


@pytest.fixture()
def clear_test_data_db():
    song_name = "8232392323623823723989"
    response = client.delete(f"/canciones/{song_name}")

    yield
    song_name = "8232392323623823723989"
    response = client.delete(f"/canciones/{song_name}")
