import json
from dataclasses import dataclass

from app.model.Genre import Genre


@dataclass
class SongBlob:

    name: str
    artist: str
    photo: str
    seconds_duration: int  # In seconds
    genre: Genre
    file: bytes
    number_of_plays: int

    def get_json(self) -> str:
        song_json = json.dumps(self.__dict__)
        return song_json
