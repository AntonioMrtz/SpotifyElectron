from dataclasses import dataclass
from typing import List


@dataclass
class User:
    name: str
    photo: str
    register_date: str
    password: bytes
    playback_history: List[str]
    playlists: List[str]
    saved_playlists: List[str]
