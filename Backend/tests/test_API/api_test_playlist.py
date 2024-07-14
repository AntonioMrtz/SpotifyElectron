from fastapi.testclient import TestClient
from httpx import Response

from app.__main__ import app

client = TestClient(app)


def create_playlist(
    name: str, descripcion: str, photo: str, headers: dict[str, str]
) -> Response:
    url = f"/playlists/?name={name}&photo={photo}&description={descripcion}"

    payload = []

    file_type_header = {"Content-Type": "application/json"}

    return client.post(url, json=payload, headers={**file_type_header, **headers})


def get_playlist(name: str, headers: dict[str, str]) -> Response:
    return client.get(f"/playlists/{name}", headers=headers)


def get_playlists(song_names: str, headers: dict[str, str]):
    return client.get(f"/playlists/selected/{song_names}", headers=headers)


def update_playlist(
    name: str, descripcion: str, photo: str, headers: dict[str, str], nuevo_nombre: str = ""
) -> Response:
    if nuevo_nombre == "":
        url = f"/playlists/{name}/?photo={photo}&description={descripcion}"

    else:
        url = f"/playlists/{name}/?photo={photo}&description={descripcion}&new_name={nuevo_nombre}"  # noqa: E501

    payload = []

    file_type_header = {"Content-Type": "application/json"}

    return client.put(url, json=payload, headers={**file_type_header, **headers})


def delete_playlist(name: str) -> Response:
    return client.delete(f"/playlists/{name}")


def get_all_playlists(headers: dict[str, str]) -> Response:
    return client.get("/playlists/", headers=headers)
