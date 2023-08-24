from main import app as app
from fastapi.testclient import TestClient


client = TestClient(app)


def create_song(
        name: str,
        file_path: str,
        artista: str,
        genero: str,
        foto: str):

    url = f"/canciones/?nombre={name}&artista={artista}&genero={genero}&foto={foto}"

    with open(file_path, 'rb') as file:
        response = client.post(url, files={'file': file})
        return response


def get_song(name: str):

    response = client.get(f"/canciones/{name}")
    return response


def delete_song(name: str):
    response = client.delete(f"/canciones/{name}")
    return response


def get_songs():
    response = client.get(f"/canciones/")
    return response


def patch_song_number_plays(name: str):

    patch_url = f"/canciones/{name}/numberOfPlays"

    response = client.patch(patch_url)
    return response
