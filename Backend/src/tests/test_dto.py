from model.Genre import Genre
from test_API.api_test_dto import get_playlist_dto, get_song_dto
from test_API.api_test_playlist import get_playlist, create_playlist, delete_playlist
from test_API.api_test_song import create_song, delete_song
from test_API.api_test_artist import create_artist, delete_artist
from test_API.api_token import get_user_jwt_header
import logging
import pytest

# * Playlist DTO


def test_get_playlist_dto_correct(clear_test_playlist_db):

    name = "8232392323623823723"
    descripcion = "descripcion"
    foto = "https://foto"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=owner,password=password)

    res_create_playlist = create_playlist(
        name=name, descripcion=descripcion, foto=foto,headers=jwt_headers)
    assert res_create_playlist.status_code == 201

    res_get_playlist = get_playlist_dto(name=name,headers=jwt_headers)
    assert res_get_playlist.status_code == 200
    assert res_get_playlist.json()["name"] == name
    assert res_get_playlist.json()["photo"] == foto
    assert res_get_playlist.json()["description"] == descripcion
    assert res_get_playlist.json()["owner"] == owner

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == 202

    res_delete_playlist = delete_playlist(name=name)
    assert res_delete_playlist.status_code == 202


def test_get_playlist_dto_not_found(clear_test_playlist_db):

    name = "8232392323623823723"
    descripcion = "descripcion"
    foto = "https://foto"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=owner,password=password)


    res_get_playlist = get_playlist_dto(name,headers=jwt_headers)
    assert res_get_playlist.status_code == 404

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == 202


def test_get_playlist_dto_invalid_name(clear_test_playlist_db):

    name = ""

    descripcion = "descripcion"
    foto = "https://foto"
    owner = "usuarioprueba834783478923489734298"
    password = "password"

    res_create_artist = create_artist(owner, foto, password)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=owner,password=password)

    res_get_playlist = get_playlist_dto(name,jwt_headers)
    assert res_get_playlist.status_code == 404

    res_delete_artist = delete_artist(owner)
    assert res_delete_artist.status_code == 202


# * Song DTO

def test_get_song_dto_correct(clear_test_song_db):

    song_name = "8232392323623823723989"
    artista = "usuarioprueba834783478923489734298"
    genero = "Pop"
    foto = "https://foto"
    file_path = "tests/assets/song.mp3"

    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(
        name=artista, password=password, photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)

    res_create_song = create_song(
        name=song_name,
        file_path=file_path,
        genero=genero,
        foto=foto,headers=jwt_headers
    )
    assert res_create_song.status_code == 201

    res_get_song = get_song_dto(song_name,jwt_headers)
    assert res_get_song.status_code == 200

    assert res_get_song.json()["name"] == song_name
    assert res_get_song.json()["artist"] == artista
    assert res_get_song.json()["genre"] == Genre(genero).name
    assert res_get_song.json()["photo"] == foto

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202


def test_song_playlist_dto_not_found(clear_test_song_db):

    artista = "usuarioprueba834783478923489734298"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(
        name=artista, password=password, photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)

    name = "8232392323623823723"

    res_get_song = get_song_dto(name,headers=jwt_headers)
    assert res_get_song.status_code == 404

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202


def test_get_song_dto_invalid_name(clear_test_song_db):

    artista = "usuarioprueba834783478923489734298"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(
        name=artista, password=password, photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)

    name = ""

    res_get_song = get_song_dto(name,headers=jwt_headers)
    assert res_get_song.status_code == 404

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202


# * FIXTURE

@pytest.fixture()
def clear_test_playlist_db():
    new_name = "82323923236238237237"
    name = "8232392323623823723"
    song_name = "8232392323623823723989"
    artista = "usuarioprueba834783478923489734298"
    delete_playlist(name=name)
    delete_playlist(name=new_name)
    delete_artist(artista)


    yield
    new_name = "82323923236238237237"
    name = "8232392323623823723"
    song_name = "8232392323623823723989"
    artista = "usuarioprueba834783478923489734298"
    delete_playlist(name=name)
    delete_playlist(name=new_name)
    delete_artist(artista)


@pytest.fixture()
def clear_test_song_db():
    song_name = "8232392323623823723989"
    artista = "usuarioprueba834783478923489734298"
    delete_song(song_name)
    delete_artist(artista)



    yield
    song_name = "8232392323623823723989"
    artista = "usuarioprueba834783478923489734298"
    delete_song(song_name)
    delete_artist(artista)
