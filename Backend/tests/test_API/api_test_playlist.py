from fastapi.testclient import TestClient

from app.__main__ import app

client = TestClient(app)


def create_playlist(name: str, descripcion: str, foto: str, headers: dict):
    url = f"/playlists/?name={name}&photo={foto}&description={descripcion}"

    payload = []

    file_type_header = {"Content-Type": "application/json"}

    return client.post(url, json=payload, headers={**file_type_header, **headers})


def get_playlist(name: str, headers: dict):
    return client.get(f"/playlists/{name}", headers=headers)


def get_playlists(song_names: str, headers: dict):
    return client.get(f"/playlists/multiple/{song_names}", headers=headers)


def update_playlist(
    name: str, descripcion: str, foto: str, headers: dict, nuevo_nombre: str = ""
):
    if nuevo_nombre == "":
        url = f"/playlists/{name}/?photo={foto}&description={descripcion}"

    else:
        url = f"/playlists/{name}/?photo={foto}&description={descripcion}&new_name={nuevo_nombre}"

    payload = []

    file_type_header = {"Content-Type": "application/json"}

    return client.put(url, json=payload, headers={**file_type_header, **headers})


def delete_playlist(name: str):
    return client.delete(f"/playlists/{name}")


def get_all_playlists(headers: dict):
    return client.get("/playlists/", headers=headers)
