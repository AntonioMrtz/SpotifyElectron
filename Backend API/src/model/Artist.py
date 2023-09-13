from dataclasses import dataclass
from model.User import User
import json


@dataclass
class Artist(User):

    uploaded_songs: list

    def get_json(self) -> json:

        user_json = super().get_json()
        data = json.loads(user_json)

        data["uploaded_songs"] = self.uploaded_songs

        updated_json_str = json.dumps(data)
        return updated_json_str
