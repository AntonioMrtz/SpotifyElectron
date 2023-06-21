from dataclasses import dataclass

from model.Genre import Genre

@dataclass
class Song:

    name: str
    artist : str
    photo : str
    genre: Genre
    file: bytes
