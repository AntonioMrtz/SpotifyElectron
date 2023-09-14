from main import app as app
from fastapi.testclient import TestClient

client = TestClient(app)


def get_artist(name: str):

    response = client.get(f"/artistas/{name}")
    return response


def create_artist(name: str, photo: str, password: str):

    url = f"/artistas/?nombre={name}&foto={photo}&password={password}"

    response = client.post(
        url
    )

    return response


def update_artist(name: str, photo: str, playlists: list, saved_playlists: list, playback_history: list, uploaded_songs: list):

    url = f"/artistas/{name}/?foto={photo}"

    payload = {
        "historial_canciones": playback_history,
        "playlists": playlists,
        "playlists_guardadas": saved_playlists,
        "canciones_creadas": uploaded_songs
    }

    response = client.put(
        url, json=payload, headers={"Content-Type": "application/json"}
    )

    return response


def delete_artist(name: str):
    response = client.delete(f"/artistas/{name}")
    return response
