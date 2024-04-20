from fastapi.testclient import TestClient

from app.__main__ import app

client = TestClient(app)


def get_playlist_dto(name: str, headers: dict):
    return client.get(f"/playlists/dto/{name}", headers=headers)


def get_song_dto(name: str, headers: dict):
    return client.get(f"/canciones/dto/{name}", headers=headers)
