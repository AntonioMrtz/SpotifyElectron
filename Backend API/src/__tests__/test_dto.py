from fastapi.testclient import TestClient
from model.Genre import Genre
import logging
import pytest

from main import app as app

client = TestClient(app)


def test_get_playlist_dto_correct(clear_test_data_db):

    name = "8232392323623823723"
    song_name = "8232392323623823723989"
    descripcion = "descripcion"
    foto = "https://foto"


    url = f"/playlists/?nombre={name}&foto={foto}&descripcion={descripcion}"

    payload = []

    response = client.post(
        url, json=payload, headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 201

    response = client.get(f"/playlists/dto/{name}")
    assert response.status_code == 200
    assert response.json()["name"]==name
    assert response.json()["photo"]==foto
    assert response.json()["description"]==descripcion

    response = client.delete(f"/playlists/{name}")
    assert response.status_code == 202


def test_get_playlist_dto_not_found():

    name = "8232392323623823723"

    response = client.get(f"/playlists/dto/{name}")
    assert response.status_code == 404


def test_get_playlist_dto_invalid_name():

    name = ""

    response = client.get(f"/playlists/dto/{name}")
    assert response.status_code == 404


# DTOSong


def test_get_song_dto_correct():

    song_name = "8232392323623823723989"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"


    url = f"/canciones/?nombre={song_name}&artista={artista}&genero={genero}&foto={foto}"

    with open('__tests__/song.mp3', 'rb') as file:
        response = client.post(url, files={'file': file})
        assert response.status_code == 201

    response = client.get(f"/canciones/dto/{song_name}")
    assert response.status_code == 200

    assert response.json()["name"]==song_name
    assert response.json()["artist"]==artista
    assert response.json()["genre"]==Genre(genero).name
    assert response.json()["photo"]==foto

    response = client.delete(f"/canciones/{song_name}")
    assert response.status_code == 202


def test_song_playlist_dto_not_found():

    name = "8232392323623823723"

    response = client.get(f"/canciones/dto/{name}")
    assert response.status_code == 404


def test_get_song_dto_invalid_name():

    name = ""

    response = client.get(f"/canciones/dto/{name}")
    assert response.status_code == 404


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
