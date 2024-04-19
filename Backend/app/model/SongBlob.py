from dataclasses import dataclass

from app.genre.genre_schema import Genre


@dataclass
class SongBlob:
    name: str
    artist: str
    photo: str
    seconds_duration: int
    genre: Genre
    file: bytes
    number_of_plays: int
