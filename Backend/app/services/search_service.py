import app.services.artist_service as artist_service
import app.services.playlist_service as playlist_service
import app.services.user_service as user_service
from app.services.song_services.song_service_provider import get_song_service
from app.services.utils import checkValidParameterString
from fastapi import HTTPException

song_service = get_song_service()


def search_by_name(name: str) -> dict:
    """Returns items that match the given name

    Args:
        name (str): the name to match

    Raises:
        Bad Request 400 HTTPException: the given name its empty
        Bad Request 500 HTTPException: an error occurred when retrieving items

    Returns:
        dict: the items that match the name on a dict
    """

    if not checkValidParameterString(name):
        raise HTTPException(
            status_code=400, detail="El nombre por el que buscar es vacío"
        )

    items = {}

    try:
        # TODO ASYNC
        songs = song_service.search_by_name(name)
        playlists = playlist_service.search_by_name(name)
        artists = artist_service.search_by_name(name)
        users = user_service.search_by_name(name)

        # Create a dictionary to store the results
        items = {
            "artistas": artists,
            "playlists": playlists,
            "users": users,
            "songs": songs,
        }

        return items

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"No se pudieron obtener los items por nombre | {e}"
        )
