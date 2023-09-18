from main import app as app
from fastapi.testclient import TestClient

client = TestClient(app)


def patch_history_playback(user_name: str, song_name: str):
    response = client.patch(
        f"/usuarios/{user_name}/historial/?nombre_cancion={song_name}")
    return response

def patch_playlist_saved(user_name: str, playlist_name: str):
    response = client.patch(
        f"/usuarios/{user_name}/playlists_guardadas/?nombre_playlist={playlist_name}")
    return response

