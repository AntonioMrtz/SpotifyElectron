from dataclasses import dataclass
from src.model.Genre import Genre
import json


@dataclass
class SongBlob:

    name: str
    artist: str
    photo: str
    duration: int  # In seconds
    genre: Genre
    file: bytes
    number_of_plays: int

    def get_json(self) -> json:
        song_json = json.dumps(self.__dict__)
        return song_json
