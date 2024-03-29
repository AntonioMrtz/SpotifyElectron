import json
from dataclasses import dataclass
from typing import List

from app.model.model_schema import SpotifyElectronModel


@dataclass
class Playlist(SpotifyElectronModel):
    name: str
    photo: str
    description: str
    upload_date: str
    owner: str
    songs: list

    def add_songs(self, song_names: List[str]) -> None:
        self.songs.extend(song_names)

    def get_json(self) -> str:
        playlist_dict = self.__dict__

        songs_json = []

        for song in self.songs:
            song_json = song.get_json()
            songs_json.append(song_json)

        playlist_dict.pop("songs", None)
        playlist_dict["songs"] = songs_json
        playlist_json = json.dumps(playlist_dict)

        return playlist_json
