from fastapi.testclient import TestClient
from httpx import Response

from app.__main__ import app

client = TestClient(app)


def get_user(name: str, headers: dict[str, str]) -> Response:
    return client.get(f"/users/{name}", headers=headers)


def create_user(name: str, photo: str, password: str):
    url = f"/users/?name={name}&photo={photo}&password={password}"

    return client.post(url)


def update_user(  # noqa: PLR0913
    name: str,
    photo: str,
    playlists: list[str],
    saved_playlists: list[str],
    playback_history: list[str],
    headers: dict[str, str],
) -> Response:
    url = f"/users/{name}/?photo={photo}"

    payload = {
        "playback_history": playback_history,
        "playlists": playlists,
        "saved_playlists": saved_playlists,
    }

    file_type_header = {"Content-Type": "application/json"}

    return client.put(url, json=payload, headers={**file_type_header, **headers})


def delete_user(name: str) -> Response:
    return client.delete(f"/users/{name}")


def patch_history_playback(user_name: str, song_name: str) -> Response:
    return client.patch(f"/users/{user_name}/playback_history/?song_name={song_name}")
