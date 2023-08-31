from dataclasses import dataclass
import json


@dataclass
class User:

    name: str
    photo: str
    register_date: str
    """ Stores the last 5 songs that the user played """
    playback_history: list
    password: str
    playlists: list
    saved_playlists: list

    def get_json(self) -> json:
        user_json = json.dumps(self.__dict__)
        return user_json
