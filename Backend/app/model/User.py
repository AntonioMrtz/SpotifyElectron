from dataclasses import dataclass


@dataclass
class User:
    name: str
    photo: str
    register_date: str
    password: bytes
    playback_history: list[str]
    playlists: list[str]
    saved_playlists: list[str]
