from dataclasses import dataclass

from app.genre.genre_schema import Genre


@dataclass
class SongDTO:
    name: str
    artist: str
    photo: str
    seconds_duration: int
    genre: Genre
    number_of_plays: int
