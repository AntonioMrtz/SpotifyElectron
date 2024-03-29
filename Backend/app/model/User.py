import json
from dataclasses import dataclass
from typing import List

from app.model.model_schema import SpotifyElectronModel


@dataclass
class User(SpotifyElectronModel):
    name: str
    photo: str
    register_date: str
    password: bytes
    playback_history: List[str]
    playlists: List[str]
    saved_playlists: List[str]

    def get_json(self) -> str:
        user_dict = self.__dict__
        user_dict.pop("password")
        user_json = json.dumps(user_dict)
        return user_json
