from dataclasses import dataclass
import services.song_service as song_service
import json


@dataclass
class PlaylistDTO:

    name: str
    photo: str
    song_names: list

    def add_songs(self,song_names: str) -> None:

        self.song_names.extends(song_names)

    def get_json(self) -> json:

        playlist_dict = self.__dict__

        playlist_json = json.dumps(playlist_dict)

        return playlist_json
