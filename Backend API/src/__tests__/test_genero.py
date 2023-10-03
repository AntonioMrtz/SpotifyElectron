from fastapi.testclient import TestClient
from test_API.api_token import get_user_jwt_header
from test_API.api_test_artist import create_artist,delete_artist

from main import app as app

client = TestClient(app)


def test_get_generos_correct():

    artista = "artista"
    foto = "https://foto"
    password = "hola"

    res_create_artist = create_artist(name=artista,password=password,photo=foto)
    assert res_create_artist.status_code == 201

    jwt_headers = get_user_jwt_header(username=artista,password=password)

    response = client.get(f"/generos/",headers=jwt_headers)
    assert response.status_code == 200

    res_delete_artist = delete_artist(artista)
    assert res_delete_artist.status_code == 202
