from dataclasses import dataclass
from typing import List


@dataclass
class Playlist:
    name: str
    photo: str
    description: str
    upload_date: str
    owner: str
    song_names: List[str]
