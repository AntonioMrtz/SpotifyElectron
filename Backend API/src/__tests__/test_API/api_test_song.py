from main import app as app
from fastapi.testclient import TestClient


client = TestClient(app)


def create_song(
        name: str,
        file_path: str,
        genero: str,
        foto: str,
        headers: dict):

    url = f"/canciones/?nombre={name}&genero={genero}&foto={foto}"

    with open(file_path, 'rb') as file:
        response = client.post(url, files={'file': file}, headers=headers)
        return response


def get_song(name: str, headers: dict):

    response = client.get(f"/canciones/{name}", headers=headers)
    return response


def delete_song(name: str):
    response = client.delete(f"/canciones/{name}")
    return response


def get_songs(headers: dict):
    response = client.get(f"/canciones/", headers=headers)
    return response


def patch_song_number_plays(name: str, headers: dict):

    patch_url = f"/canciones/{name}/numberOfPlays"

    response = client.patch(patch_url, headers=headers)
    return response


def get_songs_by_genre(genre: str, headers: dict):

    get_url = f"/canciones/generos/{genre}"

    response = client.get(get_url, headers=headers)
    return response
