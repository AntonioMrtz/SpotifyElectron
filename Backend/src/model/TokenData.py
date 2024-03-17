from dataclasses import dataclass
import json

@dataclass
class TokenData():
    username: str
    role: str
    token_type : str

    def get_json(self) -> json:

        token_data_json = json.dumps(self.__dict__)
        return token_data_json
