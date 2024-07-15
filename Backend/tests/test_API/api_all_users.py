from fastapi.testclient import TestClient
from httpx import Response

from app.__main__ import app

client = TestClient(app)


def patch_history_playback(
    user_name: str, song_name: str, headers: dict[str, str]
) -> Response:
    return client.patch(
        f"/users/{user_name}/playback_history/?song_name={song_name}", headers=headers
    )


def patch_playlist_saved(
    user_name: str, playlist_name: str, headers: dict[str, str]
) -> Response:
    return client.patch(
        f"/users/{user_name}/saved_playlists/?playlist_name={playlist_name}",
        headers=headers,
    )


def delete_playlist_saved(
    user_name: str, playlist_name: str, headers: dict[str, str]
) -> Response:
    return client.delete(
        f"/users/{user_name}/saved_playlists/?playlist_name={playlist_name}",
        headers=headers,
    )


def whoami(token: str):
    headers = {"Authorization": f"Bearer {token}"}

    return client.get("/users/whoami", headers=headers)
