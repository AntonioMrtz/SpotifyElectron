from dataclasses import dataclass

from app.spotify_electron.user.user_schema import User


@dataclass
class Artist(User):
    # TODO docstirng
    uploaded_songs: list[str]
