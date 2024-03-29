from typing import List
import json
from dataclasses import dataclass


@dataclass
class PlaylistDTO:
    name: str
    photo: str
    description: str
    upload_date: str
    owner: str
    song_names: List[str]

    def add_songs(self, song_names: List[str]) -> None:
        self.song_names.extend(song_names)

    def get_json(self) -> str:
        playlist_dict = self.__dict__

        playlist_json = json.dumps(playlist_dict)

        return playlist_json
