from fastapi.testclient import TestClient

from app.__main__ import app

client = TestClient(app)


def create_song(name: str, file_path: str, genre: str, photo: str, headers: dict):
    url = f"/songs/?name={name}&genre={genre}&photo={photo}"

    with open(file_path, "rb") as file:
        return client.post(url, files={"file": file}, headers=headers)


def get_song(name: str, headers: dict):
    return client.get(f"/songs/{name}", headers=headers)


def delete_song(name: str):
    return client.delete(f"/songs/{name}")


def get_songs(headers: dict):
    return client.get("/songs/", headers=headers)


def increase_song_streams(name: str, headers: dict):
    patch_url = f"/songs/{name}/streams"

    return client.patch(patch_url, headers=headers)


def get_songs_by_genre(genre: str, headers: dict):
    get_url = f"/songs/genres/{genre}"

    return client.get(get_url, headers=headers)


def get_song_metadata(name: str, headers: dict):
    return client.get(f"/canciones/metadata/{name}", headers=headers)
