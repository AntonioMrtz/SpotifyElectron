from dataclasses import dataclass
from typing import List

from app.model.User import User


@dataclass
class Artist(User):
    uploaded_songs: List[str]
