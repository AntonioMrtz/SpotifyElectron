from main import app as app
from fastapi.testclient import TestClient


client = TestClient(app)


def create_playlist(name: str, descripcion: str, foto: str, headers: dict):

    url = f"/playlists/?nombre={name}&foto={foto}&descripcion={descripcion}"

    payload = []

    file_type_header = {"Content-Type": "application/json"}

    response = client.post(
        url, json=payload, headers={**file_type_header, **headers}
    )

    return response


def get_playlist(name: str, headers: dict):

    response = client.get(f"/playlists/{name}", headers=headers)
    return response


def get_playlists(song_names: str, headers: dict):

    response = client.get(f"/playlists/multiple/{song_names}", headers=headers)
    return response


def update_playlist(
        name: str,
        descripcion: str,
        foto: str,
        headers: dict,
        nuevo_nombre: str = ""
        ):

    if nuevo_nombre == "":
        url = f"/playlists/{name}/?foto={foto}&descripcion={descripcion}"

    else:
        url = f"/playlists/{name}/?foto={foto}&descripcion={descripcion}&nuevo_nombre={nuevo_nombre}"

    payload = []

    file_type_header = {"Content-Type": "application/json"}

    response = client.put(
        url, json=payload, headers={**file_type_header, **headers}
    )

    return response


def delete_playlist(name: str):
    response = client.delete(f"/playlists/{name}")
    return response


def get_all_playlists(headers:dict):
    response = client.get(f"/playlists/",headers=headers)
    return response
