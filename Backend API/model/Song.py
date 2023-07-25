from dataclasses import dataclass
from model.Genre import Genre
import json


@dataclass
class Song:

    name: str
    artist: str
    photo: str
    """ In seconds """
    duration : int
    genre: Genre
    file: bytes

    def get_json(self) -> json:
        song_json = json.dumps(self.__dict__)
        return song_json
