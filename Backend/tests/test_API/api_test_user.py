from fastapi.testclient import TestClient

from app.__main__ import app

client = TestClient(app)


def get_user(name: str, headers: dict):
    return client.get(f"/usuarios/{name}", headers=headers)


def create_user(name: str, photo: str, password: str):
    url = f"/usuarios/?nombre={name}&foto={photo}&password={password}"

    return client.post(url)


def update_user(
    name: str,
    photo: str,
    playlists: list,
    saved_playlists: list,
    playback_history: list,
    headers: dict,
):
    url = f"/usuarios/{name}/?foto={photo}"

    payload = {
        "historial_canciones": playback_history,
        "playlists": playlists,
        "playlists_guardadas": saved_playlists,
    }

    file_type_header = {"Content-Type": "application/json"}

    return client.put(url, json=payload, headers={**file_type_header, **headers})


def delete_user(name: str):
    return client.delete(f"/usuarios/{name}")


def patch_history_playback(user_name: str, song_name: str):
    return client.patch(f"/usuarios/{user_name}/historial/?nombre_cancion={song_name}")
