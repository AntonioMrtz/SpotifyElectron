import json
from dataclasses import dataclass

from app.model.model_schema import SpotifyElectronModel


@dataclass
class TokenData(SpotifyElectronModel):
    username: str
    role: str
    token_type: str

    def get_json(self) -> str:
        token_data_json = json.dumps(self.__dict__)
        return token_data_json
