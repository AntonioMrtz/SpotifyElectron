from dataclasses import dataclass

from app.genre.genre_schema import Genre


@dataclass
class Song:
    name: str
    artist: str
    photo: str
    seconds_duration: int
    genre: Genre
    url: str
    number_of_plays: int
