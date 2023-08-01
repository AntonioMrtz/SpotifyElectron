from fastapi.testclient import TestClient
import logging
import pytest

from main import app as app

client = TestClient(app)


def test_get_playlist_dto_correct(clear_test_data_db):

    name = "8232392323623823723"

    url = f"/playlists/?nombre={name}&foto=foto&descripcion=descripcion"

    payload = []

    response = client.post(
        url, json=payload, headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 201

    response = client.get(f"/playlists/dto/{name}")
    assert response.status_code == 200

    response = client.delete(f"/playlists/{name}")
    assert response.status_code == 202


def test_get_playlist_playlist_dto_not_found():

    name = "8232392323623823723"

    response = client.get(f"/playlists/dto/{name}")
    assert response.status_code == 404


def test_get_playlist_playlist_dto_invalid_name():

    name = ""

    response = client.get(f"/playlists/dto/{name}")
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
