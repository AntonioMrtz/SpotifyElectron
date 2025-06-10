from fastapi.testclient import TestClient
from httpx import Response

from app.__main__ import app
from tests.test_API.api_token import get_user_jwt_header

client = TestClient(app)


def create_playlist(
    name: str, descripcion: str, photo: str, headers: dict[str, str]
) -> Response:
    url = f"/playlists/?name={name}&photo={photo}&description={descripcion}"

    payload = []

    file_type_header = {"Content-Type": "application/json"}

    return client.post(url, json=payload, headers={**file_type_header, **headers})


def get_playlist(name: str, headers: dict[str, str]) -> Response:
    return client.get(f"/playlists/{name}", headers=headers)


def get_playlists(song_names: str, headers: dict[str, str]):
    return client.get(f"/playlists/selected/{song_names}", headers=headers)


def update_playlist(
    name: str,
    descripcion: str,
    photo: str,
    headers: dict[str, str],
    nuevo_nombre: str = "",
) -> Response:
    if nuevo_nombre == "":
        url = f"/playlists/{name}/?photo={photo}&description={descripcion}"

    else:
        url = f"/playlists/{name}/?photo={photo}&description={descripcion}&new_name={nuevo_nombre}"  # noqa: E501

    payload = []

    file_type_header = {"Content-Type": "application/json"}

    return client.put(url, json=payload, headers={**file_type_header, **headers})


def update_playlist_metadata(
    name: str,
    headers: dict[str, str],
    description: str = None,
    photo: str = None,
    new_name: str = None,
    is_collaborative: bool = None,
    is_public: bool = None,
) -> Response:
    """Update playlist metadata fields.
    
    Args:
        name: Current playlist name
        headers: JWT headers for authentication
        description: Optional new description
        photo: Optional new photo URL
        new_name: Optional new name for the playlist
        is_collaborative: Optional new collaborative status
        is_public: Optional new public status
        
    Returns:
        Response from the API
    """
    url = f"/playlists/{name}/metadata"
    params = {}
    
    if new_name:
        params["new_name"] = new_name
    if description is not None:
        params["description"] = description
    if photo is not None:
        params["photo"] = photo
    if is_collaborative is not None:
        params["is_collaborative"] = str(is_collaborative).lower()
    if is_public is not None:
        params["is_public"] = str(is_public).lower()
        
    file_type_header = {"Content-Type": "application/json"}
    
    return client.patch(
        url,
        params=params,
        headers={**file_type_header, **headers}
    )


def delete_playlist(name: str) -> Response:
    return client.delete(f"/playlists/{name}")


def get_all_playlists(headers: dict[str, str]) -> Response:
    return client.get("/playlists/", headers=headers)


def add_songs_to_playlist(
    name: str,
    song_names: list[str],
    headers: dict[str, str],
) -> Response:
    return client.patch(f"/playlists/{name}/songs", headers=headers, json=song_names)


def remove_song_from_playlist(
    name: str,
    song_names: list[str],
    headers: dict[str, str],
) -> Response:
    return client.delete(
        f"/playlists/{name}/songs/", params={"song_names": song_names}, headers=headers
    )


def create_basic_playlist(name: str, owner: str) -> Response:
    """Helper function to create a basic playlist for testing.
    
    Args:
        name: Name of the playlist
        owner: Owner of the playlist
        
    Returns:
        Response from the API
    """
    photo = "https://example.com/photo.jpg"
    description = "Test playlist"
    jwt_headers = get_user_jwt_header(username=owner, password="password")
    
    return create_playlist(
        name=name,
        descripcion=description,
        photo=photo,
        headers=jwt_headers
    )
