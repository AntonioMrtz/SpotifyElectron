from main import app as app
from fastapi.testclient import TestClient

client = TestClient(app)


def get_artist(name: str, headers: dict):

    response = client.get(f"/artistas/{name}", headers=headers)
    return response


def create_artist(name: str, photo: str, password: str):

    url = f"/artistas/?nombre={name}&foto={photo}&password={password}"

    response = client.post(
        url
    )

    return response


def update_artist(name: str, photo: str, playlists: list, saved_playlists: list, playback_history: list, uploaded_songs: list, headers: dict):

    url = f"/artistas/{name}/?foto={photo}"

    payload = {
        "historial_canciones": playback_history,
        "playlists": playlists,
        "playlists_guardadas": saved_playlists,
        "canciones_creadas": uploaded_songs
    }

    file_type_header = {"Content-Type": "application/json"}

    response = client.put(
        url, json=payload, headers={**file_type_header, **headers}
    )

    return response


def delete_artist(name: str):
    response = client.delete(f"/artistas/{name}")
    return response


def get_artists(headers: dict):
    response = client.get(f"/artistas/", headers=headers)
    return response


def get_play_count_artist(name: str, headers: dict):
    response = client.get(f"/artistas/{name}/reproducciones", headers=headers)
    return response
