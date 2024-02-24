from main import app as app
from fastapi.testclient import TestClient

client = TestClient(app)


def patch_history_playback(user_name: str, song_name: str, headers: dict):
    response = client.patch(
        f"/usuarios/{user_name}/historial/?nombre_cancion={song_name}", headers=headers)
    return response


def patch_playlist_saved(user_name: str, playlist_name: str, headers: dict):
    response = client.patch(
        f"/usuarios/{user_name}/playlists_guardadas/?nombre_playlist={playlist_name}", headers=headers)
    return response


def delete_playlist_saved(user_name: str, playlist_name: str, headers: dict):
    response = client.delete(
        f"/usuarios/{user_name}/playlists_guardadas/?nombre_playlist={playlist_name}", headers=headers)
    return response


def whoami(token: str):

    headers = {
        "Authorization": f"{token}"
    }

    response = client.get(
        f"/usuarios/whoami", headers=headers)
    return response
