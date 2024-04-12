from dataclasses import dataclass


@dataclass
class Playlist:
    name: str
    photo: str
    description: str
    upload_date: str
    owner: str
    song_names: list[str]
