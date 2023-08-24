from main import app as app
from fastapi.testclient import TestClient


client = TestClient(app)


def get_playlist_dto(name: str):

    response = client.get(f"/playlists/dto/{name}")
    return response


def get_song_dto(name: str):
    response = client.get(f"/canciones/dto/{name}")
    return response
