from dataclasses import dataclass
import json


@dataclass
class User:

    name: str
    photo: str
    register_date: str
    password: str
    playback_history: list
    playlists: list
    saved_playlists: list

    def get_json(self) -> json:

        self.password= self.password.decode('utf-8')
        user_json = json.dumps(self.__dict__)
        return user_json
