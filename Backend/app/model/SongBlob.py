from dataclasses import dataclass

from app.model.Genre import Genre


@dataclass
class SongBlob:
    name: str
    artist: str
    photo: str
    seconds_duration: int
    genre: Genre
    file: bytes
    number_of_plays: int
