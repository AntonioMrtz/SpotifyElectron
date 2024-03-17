import json
from dataclasses import dataclass


@dataclass
class PlaylistDTO:
    name: str
    photo: str
    description: str
    upload_date: str
    owner: str
    song_names: list

    def add_songs(self, song_names: str) -> None:
        self.song_names.extends(song_names)

    def get_json(self) -> str:
        playlist_dict = self.__dict__

        playlist_json = json.dumps(playlist_dict)

        return playlist_json
