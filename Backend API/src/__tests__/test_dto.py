from fastapi.testclient import TestClient
from model.Genre import Genre
from test_API.api_test_dto import get_playlist_dto, get_song_dto
from test_API.api_test_playlist import get_playlist, create_playlist, delete_playlist
from test_API.api_test_song import create_song, delete_song
import logging
import pytest

from main import app as app


# * Playlist DTO

def test_get_playlist_dto_correct(clear_test_playlist_db):

    name = "8232392323623823723"
    descripcion = "descripcion"
    foto = "https://foto"
    owner = "usuarioprueba834783478923489734298"

    res_create_playlist = create_playlist(
        name=name, descripcion=descripcion, foto=foto,creador=owner)
    assert res_create_playlist.status_code == 201

    res_get_playlist = get_playlist_dto(name=name)
    assert res_get_playlist.status_code == 200
    assert res_get_playlist.json()["name"] == name
    assert res_get_playlist.json()["photo"] == foto
    assert res_get_playlist.json()["description"] == descripcion
    assert res_get_playlist.json()["owner"] == owner

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == 202


def test_get_playlist_dto_not_found():

    name = "8232392323623823723"

    res_get_playlist = get_playlist_dto(name)
    assert res_get_playlist.status_code == 404


def test_get_playlist_dto_invalid_name():

    name = ""

    res_get_playlist = get_playlist_dto(name)
    assert res_get_playlist.status_code == 404


# * Song DTO

def test_get_song_dto_correct(clear_test_song_db):

    song_name = "8232392323623823723989"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"
    file_path = "__tests__/assets/song.mp3"

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        artista=artista,
        genero=genero,
        foto=foto
        )
    assert res_create_song.status_code == 201

    res_get_song = get_song_dto(song_name)
    assert res_get_song.status_code == 200

    assert res_get_song.json()["name"] == song_name
    assert res_get_song.json()["artist"] == artista
    assert res_get_song.json()["genre"] == Genre(genero).name
    assert res_get_song.json()["photo"] == foto

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202


def test_song_playlist_dto_not_found():

    name = "8232392323623823723"

    res_get_song = get_song_dto(name)
    assert res_get_song.status_code == 404


def test_get_song_dto_invalid_name():

    name = ""

    res_get_song = get_song_dto(name)
    assert res_get_song.status_code == 404


# * FIXTURE

@pytest.fixture()
def clear_test_playlist_db():
    new_name = "82323923236238237237"
    name = "8232392323623823723"
    song_name = "8232392323623823723989"
    delete_playlist(name=name)
    delete_playlist(name=new_name)

    yield
    new_name = "82323923236238237237"
    name = "8232392323623823723"
    delete_playlist(name=name)
    delete_playlist(name=new_name)


@pytest.fixture()
def clear_test_song_db():
    song_name = "8232392323623823723989"
    delete_song(song_name)

    yield
    song_name = "8232392323623823723989"
    delete_song(song_name)
