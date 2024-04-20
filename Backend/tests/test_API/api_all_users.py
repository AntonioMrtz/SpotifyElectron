from fastapi.testclient import TestClient

from app.__main__ import app

client = TestClient(app)


def patch_history_playback(user_name: str, song_name: str, headers: dict):
    return client.patch(
        f"/usuarios/{user_name}/historial/?nombre_cancion={song_name}", headers=headers
    )


def patch_playlist_saved(user_name: str, playlist_name: str, headers: dict):
    return client.patch(
        f"/usuarios/{user_name}/playlists_guardadas/?nombre_playlist={playlist_name}",
        headers=headers,
    )


def delete_playlist_saved(user_name: str, playlist_name: str, headers: dict):
    return client.delete(
        f"/usuarios/{user_name}/playlists_guardadas/?nombre_playlist={playlist_name}",
        headers=headers,
    )


def whoami(token: str):
    headers = {"Authorization": f"{token}"}

    return client.get("/usuarios/whoami", headers=headers)
