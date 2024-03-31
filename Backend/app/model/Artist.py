import json
from dataclasses import dataclass
from typing import List

from app.model.User import User


@dataclass
class Artist(User):
    uploaded_songs: List[str]

    def get_json(self) -> str:
        user_json = super().get_json()
        data = json.loads(user_json)

        data["uploaded_songs"] = self.uploaded_songs

        updated_json_str = json.dumps(data)
        return updated_json_str
