from fastapi.testclient import TestClient

from app.__main__ import app

client = TestClient(app)


def get_artist(name: str, headers: dict):
    return client.get(f"/artistas/{name}", headers=headers)


def create_artist(name: str, photo: str, password: str):
    url = f"/artistas/?nombre={name}&foto={photo}&password={password}"

    return client.post(url)


def update_artist(
    name: str,
    photo: str,
    playlists: list,
    saved_playlists: list,
    playback_history: list,
    uploaded_songs: list,
    headers: dict,
):
    url = f"/artistas/{name}/?foto={photo}"

    payload = {
        "historial_canciones": playback_history,
        "playlists": playlists,
        "playlists_guardadas": saved_playlists,
        "canciones_creadas": uploaded_songs,
    }

    file_type_header = {"Content-Type": "application/json"}

    return client.put(url, json=payload, headers={**file_type_header, **headers})


def delete_artist(name: str):
    return client.delete(f"/artistas/{name}")


def get_artists(headers: dict):
    return client.get("/artistas/", headers=headers)


def get_play_count_artist(name: str, headers: dict):
    return client.get(f"/artistas/{name}/reproducciones", headers=headers)
