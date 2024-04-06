from dataclasses import dataclass

from app.model.Genre import Genre


@dataclass
class SongDTO:
    name: str
    artist: str
    photo: str
    seconds_duration: int
    genre: Genre
    number_of_plays: int
