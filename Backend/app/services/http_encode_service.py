import json
from typing import Any

from fastapi.encoders import jsonable_encoder


def get_json(object: Any) -> str:
    # TODO
    jsonable_object = jsonable_encoder(object)
    json_object = json.dumps(jsonable_object)

    return json_object
