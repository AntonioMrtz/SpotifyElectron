from fastapi.testclient import TestClient
from httpx import Response

from app.__main__ import app

client = TestClient(app)


def get_artist(name: str, headers: dict[str, str]) -> Response:
    return client.get(f"/artists/{name}", headers=headers)


def create_artist(name: str, photo: str, password: str) -> Response:
    url = f"/artists/?name={name}&photo={photo}&password={password}"

    return client.post(url)


def update_artist(  # noqa: PLR0913
    name: str,
    photo: str,
    playlists: list[str],
    saved_playlists: list[str],
    playback_history: list[str],
    uploaded_songs: list[str],
    headers: dict[str, str],
) -> Response:
    url = f"/artists/{name}/?photo={photo}"

    payload = {
        "playback_history": playback_history,
        "playlists": playlists,
        "saved_playlists": saved_playlists,
        "uploaded_songs": uploaded_songs,
    }

    file_type_header = {"Content-Type": "application/json"}

    return client.put(url, json=payload, headers={**file_type_header, **headers})


def get_artists(headers: dict[str, str]) -> Response:
    return client.get("/artists/", headers=headers)


def get_artist_streams(name: str, headers: dict[str, str]) -> Response:
    return client.get(f"/artists/{name}/streams", headers=headers)
