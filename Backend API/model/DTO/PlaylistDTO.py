from dataclasses import dataclass
from datetime import date
import services.song_service as song_service
import json


@dataclass
class PlaylistDTO:

    name: str
    photo: str
    song_names: list
    fecha_adicion: date

    def add_songs(song_names: list) -> None:

        self.song_names.extends(song_names)

    def get_json(self) -> json:

        playlist_dict = self.__dict__

        playlist_json = json.dumps(playlist_dict)

        return playlist_json
