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
    name: str,
    descripcion: str,
    photo: str,
    headers: dict[str, str],
    nuevo_nombre: str = "",
) -> Response:
    if nuevo_nombre == "":
        url = f"/playlists/{name}/?photo={photo}&description={descripcion}"

    else:
        url = f"/playlists/{name}/?photo={photo}&description={descripcion}&new_name={nuevo_nombre}"  # noqa: E501

    payload = []

    file_type_header = {"Content-Type": "application/json"}

    return client.put(url, json=payload, headers={**file_type_header, **headers})


def update_playlist_metadata(
    name: str,
    descripcion: str = None,
    photo: str = None,
    headers: dict[str, str] = None,
    nuevo_nombre: str = None,
) -> Response:
    url = f"/playlists/{name}/metadata"
    params = {}
    if nuevo_nombre:
        params["new_name"] = nuevo_nombre
    if descripcion is not None:
        params["description"] = descripcion
    if photo is not None:
        params["photo"] = photo
    file_type_header = {"Content-Type": "application/json"}
    return client.patch(url, params=params, headers={**file_type_header, **(headers or {})})


def delete_playlist(name: str) -> Response:
    return client.delete(f"/playlists/{name}")


def get_all_playlists(headers: dict[str, str]) -> Response:
    return client.get("/playlists/", headers=headers)


def add_songs_to_playlist(
    name: str,
    song_names: list[str],
    headers: dict[str, str],
) -> Response:
    return client.patch(f"/playlists/{name}/songs", headers=headers, json=song_names)


def remove_song_from_playlist(
    name: str,
    song_names: list[str],
    headers: dict[str, str],
) -> Response:
    return client.delete(
        f"/playlists/{name}/songs/", params={"song_names": song_names}, headers=headers
    )
