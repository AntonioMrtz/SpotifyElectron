from fastapi.testclient import TestClient
from pytest import fixture, raises
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED

from app.__main__ import app
from app.spotify_electron.genre.genre_schema import Genre, GenreNotValidException
from tests.test_API.api_test_artist import create_artist
from tests.test_API.api_test_user import delete_user
from tests.test_API.api_token import get_user_jwt_header

client = TestClient(app)


@fixture(scope="module", autouse=True)
def set_up(trigger_app_startup):
    pass


def test_get_genres_correct():
    artista = "artista"
    photo = "https://photo"
    password = "hola"

    res_create_artist = create_artist(name=artista, password=password, photo=photo)
    assert res_create_artist.status_code == HTTP_201_CREATED

    jwt_headers = get_user_jwt_header(username=artista, password=password)

    response = client.get("/genres/", headers=jwt_headers)
    assert response.status_code == HTTP_200_OK
    assert isinstance(response.json(), dict)

    genre_dict: dict = response.json()
    for genre in Genre:
        assert genre.value in genre_dict.values()

    res_delete_artist = delete_user(artista)
    assert res_delete_artist.status_code == HTTP_202_ACCEPTED


def test_check_genre_valid():
    valid_genre = Genre.AMBIENT
    assert Genre.check_valid_genre(valid_genre.value)


def test_check_genre_invalid():
    invalid_genre = "invalid_genre"
    with raises(GenreNotValidException):
        Genre.check_valid_genre(invalid_genre)
