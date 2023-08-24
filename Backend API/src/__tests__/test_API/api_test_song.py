from main import app as app
from fastapi.testclient import TestClient


client = TestClient(app)


def create_song(
        name: str,
        file_path: str,
        artista: str,
        genero: str,
        foto: str):
    name = "8232392323623823723989"
    artista = "artista"
    genero = "Pop"
    foto = "https://foto"

    url = f"/canciones/?nombre={name}&artista={artista}&genero={genero}&foto={foto}"

    with open(file_path, 'rb') as file:
        response = client.post(url, files={'file': file})
        return response


def delete_song(name: str):
    response = client.delete(f"/canciones/{name}")
    return response
