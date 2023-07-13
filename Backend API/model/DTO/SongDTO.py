from dataclasses import dataclass
from model.Genre import Genre
import json


@dataclass
class SongDTO:

    name: str
    artist: str
    photo: str
    genre: Genre

    def get_json(self) -> json:
        song_json = json.dumps(self.__dict__)
        return song_json
