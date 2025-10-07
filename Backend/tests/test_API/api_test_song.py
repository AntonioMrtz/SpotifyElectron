from fastapi.testclient import TestClient
from httpx import Response

from io import BytesIO

from app.__main__ import app

client = TestClient(app)


def create_song(
    name: str, file_path: str, genre: str, photo: str, headers: dict[str, str]
) -> Response:
    url = f"/songs/?name={name}&genre={genre}&photo={photo}"

    with open(file_path, "rb") as file:
        return client.post(url, files={"file": file}, headers=headers)


def get_song(name: str, headers: dict[str, str]) -> Response:
    return client.get(f"/songs/{name}", headers=headers)


def delete_song(name: str) -> Response:
    return client.delete(f"/songs/{name}")


def get_songs(headers: dict[str, str]) -> Response:
    return client.get("/songs/", headers=headers)


def increase_song_streams(name: str, headers: dict[str, str]) -> Response:
    patch_url = f"/songs/{name}/streams"

    return client.patch(patch_url, headers=headers)


def get_songs_by_genre(genre: str, headers: dict[str, str]) -> Response:
    get_url = f"/songs/genres/{genre}"

    return client.get(get_url, headers=headers)


def get_song_metadata(name: str, headers: dict[str, str]) -> Response:
    return client.get(f"/songs/metadata/{name}", headers=headers)



def test_create_song_success(name: str, file_path: str, genre: str, photo: str, headers: dict[str, str]):
    response = create_song(name, file_path, genre, photo, headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == name
    assert data["genre"] == genre
    assert "id" in data  # check the response includes an id

def test_create_song_invalid_file(headers):
    # Fake bytes for a non-audio file
    fake_file = BytesIO(b"this is not audio")
    response = client.post(
        "/songs/?name=BadSong&genre=Pop&photo=url",
        files={"file": ("fake.txt", fake_file)},
        headers=headers
    )
    assert response.status_code == 400
    assert "wrong file type" in response.text


def test_create_song_duplicate(headers):
    file_path = "tests/assets/song_4_seconds.mp3"
    create_song("DuplicateSong", file_path, "Pop", "some_photo", headers)
    
    # Try creating again
    response = create_song("DuplicateSong", file_path, "Pop", "some_photo", headers)
    assert response.status_code == 409  # or whatever your API returns for duplicate




