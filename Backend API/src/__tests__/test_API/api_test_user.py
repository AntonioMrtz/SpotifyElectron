from main import app as app
from fastapi.testclient import TestClient

client = TestClient(app)

def get_user(name: str):

    response = client.get(f"/usuarios/{name}")
    return response

def create_user(name: str, photo: str, password: str):

    url = f"/usuarios/?nombre={name}&foto={photo}&password={password}"

    response = client.post(
        url
    )

    return response


def delete_user(name: str):
    response = client.delete(f"/usuarios/{name}")
    return response
