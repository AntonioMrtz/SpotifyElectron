from main import app as app
from fastapi.testclient import TestClient


client = TestClient(app)


# * PLAYLIST

def create_playlist(name: str, descripcion: str, foto: str):

    url = f"/playlists/?nombre={name}&foto={foto}&descripcion={descripcion}"

    payload = []

    response = client.post(
        url, json=payload, headers={"Content-Type": "application/json"}
    )

    return response


def get_playlist(name: str):

    response = client.get(f"/playlists/{name}")
    return response


def update_playlist(
        name: str,
        descripcion: str,
        foto: str,
        nuevo_nombre: str = ""):

    if nuevo_nombre == "":
        url = f"/playlists/{name}/?foto={foto}&descripcion={descripcion}"

    else:
        url = f"/playlists/{name}/?foto={foto}&descripcion={descripcion}&nuevo_nombre={nuevo_nombre}"

    payload = []

    response = client.put(
        url, json=payload, headers={"Content-Type": "application/json"}
    )

    return response


def delete_playlist(name: str):
    response = client.delete(f"/playlists/{name}")
    return response


# * SONG

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


# * DTO

def get_playlist_dto(name: str):

    response = client.get(f"/playlists/dto/{name}")
    return response


def get_song_dto(name: str):
    response = client.get(f"/canciones/dto/{name}")
    return response
