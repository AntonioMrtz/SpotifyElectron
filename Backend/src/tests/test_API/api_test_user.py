from main import app as app
from fastapi.testclient import TestClient

client = TestClient(app)


def get_user(name: str, headers: dict):

    response = client.get(f"/usuarios/{name}", headers=headers)
    return response


def create_user(name: str, photo: str, password: str):

    url = f"/usuarios/?nombre={name}&foto={photo}&password={password}"

    response = client.post(
        url
    )

    return response


def update_user(name: str, photo: str, playlists: list, saved_playlists: list, playback_history: list, headers: dict):

    url = f"/usuarios/{name}/?foto={photo}"

    payload = {
        "historial_canciones": playback_history,
        "playlists": playlists,
        "playlists_guardadas": saved_playlists
    }

    file_type_header = {"Content-Type": "application/json"}

    response = client.put(
        url, json=payload, headers={**file_type_header, **headers}
    )

    return response


def delete_user(name: str):
    response = client.delete(f"/usuarios/{name}")
    return response


def patch_history_playback(user_name: str, song_name: str):
    response = client.patch(
        f"/usuarios/{user_name}/historial/?nombre_cancion={song_name}")
    return response
