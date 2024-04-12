from fastapi.testclient import TestClient
from pytest import fixture
from test_API.api_test_artist import create_artist, delete_artist
from test_API.api_token import get_user_jwt_header

from app.__main__ import app
from app.model.Genre import Genre

client = TestClient(app)


@fixture(scope="module", autouse=True)
def set_up(trigger_app_start):
    pass


def test_get_generos_correct():
    artista = "artista"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    response = client.get("/generos/", headers=jwt_headers)
    assert response.status_code == 200

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202


def test_check_valid_genre_correct():
    valid_genre = Genre.AMBIENT
    assert Genre.check_valid_genre(valid_genre.value)


def test_check_valid_genre_invalid():
    invalid_genre = "invalid_genre"
    assert not Genre.check_valid_genre(invalid_genre)
