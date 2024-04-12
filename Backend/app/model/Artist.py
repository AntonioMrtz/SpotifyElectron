from dataclasses import dataclass

from app.model.User import User


@dataclass
class Artist(User):
    uploaded_songs: list[str]
