from model.Genre import Genre
from test_API.api_test_song import create_song,delete_song,get_song,get_songs,patch_song_number_plays,get_songs_by_genre
from test_API.api_test_artist import get_artist,create_artist,delete_artist
from test_API.api_test_user import create_user,delete_user
from test_API.api_token import get_user_jwt_header
import json
import pytest


def test_post_cancion_correct(clear_test_data_db):

    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)

    res_create_song = create_song(name=song_name,file_path=file_path,genero=genero,foto=foto,headers=jwt_headers)
    assert res_create_song.status_code == 201

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202

def test_post_cancion_user_as_artist(clear_test_data_db):

    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    username = "artista"
    genero = "Pop"
    foto = "https://foto"
    password = "hola"

    res_create_user = create_user(name=username,password=password,photo=foto)
    assert res_create_user.status_code == 201

    jwt_headers = get_user_jwt_header(username=username,password=password)

    res_create_song = create_song(name=song_name,file_path=file_path,genero=genero,foto=foto,headers=jwt_headers)
    assert res_create_song.status_code == 404


def test_post_cancion_correct_check_valid_duration(clear_test_data_db):

    song_name = "8232392323623823723989"
    file_path = "tests/assets/song_4_seconds.mp3"
    artista = "artista"
    genero = "Pop"

    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)


    res_create_song = create_song(name=song_name,file_path=file_path,genero=genero,foto=foto,headers=jwt_headers)
    assert res_create_song.status_code == 201

    res_get_song = get_song(name=song_name,headers=jwt_headers)
    assert res_get_song.status_code == 200
    assert "4" == str(res_get_song.json()["duration"]).split(".")[0]


    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202


def test_post_cancion_correct_check_invalid_duration(clear_test_data_db):


    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genero = "Pop"

    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)


    res_create_song = create_song(name=song_name,file_path=file_path,genero=genero,foto=foto,headers=jwt_headers)
    assert res_create_song.status_code == 201

    res_get_song = get_song(name=song_name,headers=jwt_headers)
    assert res_get_song.status_code == 200
    assert "0" in str(res_get_song.json()["duration"])

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202



def test_get_cancion_correct(clear_test_data_db):

    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"

    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)


    res_create_song = create_song(name=song_name,file_path=file_path,genero=genero,foto=foto,headers=jwt_headers)
    assert res_create_song.status_code == 201

    res_get_song = get_song(name=song_name,headers=jwt_headers)
    assert res_get_song.status_code == 200
    assert res_get_song.json()["name"]==song_name
    assert res_get_song.json()["artist"]==artista
    assert res_get_song.json()["genre"]==Genre(genero).name
    assert res_get_song.json()["photo"]==foto


    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202




def test_get_cancion_invalid_name(clear_test_data_db):


    artista = "artista"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)

    song_name = "8232392323623823723989"

    res_get_song = get_song(name=song_name,headers=jwt_headers)
    assert res_get_song.status_code == 404


    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202


def test_delete_cancion_correct(clear_test_data_db):

    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"

    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)


    res_create_song = create_song(name=song_name,file_path=file_path,genero=genero,foto=foto,headers=jwt_headers)
    assert res_create_song.status_code == 201


    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202



def test_delete_cancion_not_found():

    song_name = "8232392323623823723989"

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 404


def test_get_canciones_correct(clear_test_data_db):


    artista = "artista"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)

    res_get_songs = get_songs(headers=jwt_headers)
    assert res_get_songs.status_code == 200

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202



def test_patch_number_plays_cancion_correct(clear_test_data_db):

    song_name = "8232392323623823723989"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"
    file_path = "tests/assets/song.mp3"

    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)


    res_create_song = create_song(name=song_name,file_path=file_path,genero=genero,foto=foto,headers=jwt_headers)
    assert res_create_song.status_code == 201

    res_patch_song = patch_song_number_plays(name=song_name,headers=jwt_headers)
    assert res_patch_song.status_code==204

    res_get_song = get_song(name=song_name,headers=jwt_headers)
    assert res_get_song.status_code == 200
    assert res_get_song.json()["name"]==song_name
    assert res_get_song.json()["artist"]==artista
    assert res_get_song.json()["genre"]==Genre(genero).name
    assert res_get_song.json()["photo"]==foto
    assert res_get_song.json()["number_of_plays"]==1


    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202



def test_patch_song_not_found(clear_test_data_db):

    song_name = "8232392323623823723989"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"
    file_path = "tests/assets/song.mp3"

    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)

    song_name = "8232392323623823723989"

    res_patch_song = patch_song_number_plays(name=song_name,headers=jwt_headers)
    assert res_patch_song.status_code==404


def test_patch_song_invalid_name(clear_test_data_db):

    song_name = "8232392323623823723989"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"
    file_path = "tests/assets/song.mp3"

    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)

    song_name = ""

    res_patch_song = patch_song_number_plays(name=song_name,headers=jwt_headers)
    assert res_patch_song.status_code==404


def test_post_song_uploaded_songs_updated(clear_test_data_db):

    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)

    res_create_song = create_song(name=song_name,file_path=file_path,genero=genero,foto=foto,headers=jwt_headers)
    assert res_create_song.status_code == 201

    res_get_artist = get_artist(name=artista,headers=jwt_headers)
    assert res_get_artist.status_code == 200
    assert len(res_get_artist.json()["uploaded_songs"])==1
    assert res_get_artist.json()["uploaded_songs"][0]==song_name

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202

def test_post_song_uploaded_songs_bad_artist(clear_test_data_db):

    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202

    res_create_song = create_song(name=song_name,file_path=file_path,genero=genero,foto=foto,headers=jwt_headers)
    assert res_create_song.status_code == 404

def test_delete_song_uploaded_songs_updated(clear_test_data_db):

    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)

    res_create_song = create_song(name=song_name,file_path=file_path,genero=genero,foto=foto,headers=jwt_headers)
    assert res_create_song.status_code == 201


    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202

    res_get_artist = get_artist(name=artista,headers=jwt_headers)
    assert res_get_artist.status_code == 200
    assert len(res_get_artist.json()["uploaded_songs"])==0

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202

def test_get_cancion_by_genre(clear_test_data_db):

    song_name = "8232392323623823723989"
    file_path = "tests/assets/song.mp3"
    artista = "artista"
    genero = "Rock"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)

    res_create_song = create_song(name=song_name,file_path=file_path,genero=genero,foto=foto,headers=jwt_headers)
    assert res_create_song.status_code == 201

    res_get_song_by_genre = get_songs_by_genre(genre=genero,headers=jwt_headers)
    assert res_get_song_by_genre.status_code == 200
    assert len(res_get_song_by_genre.json())==1

    res_delete_song = delete_song(song_name)
    assert res_delete_song.status_code == 202

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202

def test_get_cancion_by_genre_bad_genre(clear_test_data_db):

    genero = "RockInventado"

    artista = "artista"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)


    res_get_song_by_genre = get_songs_by_genre(genre=genero,headers=jwt_headers)
    assert res_get_song_by_genre.status_code == 422

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202



@pytest.fixture()
def clear_test_data_db():
    song_name = "8232392323623823723989"
    artista = "artista"
    delete_song(song_name)
    delete_artist(artista)
    delete_user(artista)


    yield
    song_name = "8232392323623823723989"
    artista = "artista"
    delete_song(song_name)
    delete_artist(artista)
    delete_user(artista)
