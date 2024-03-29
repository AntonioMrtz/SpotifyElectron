import json

import app.services.artist_service as artist_service
import app.services.playlist_service as playlist_service
import app.services.user_service as user_service
from fastapi import HTTPException
from app.services.song_services.song_service_provider import get_song_service
from app.services.utils import checkValidParameterString

song_service = get_song_service()


def search_by_name(name: str) -> str:
    """Returns songs, artist and playlist that matches name

    Parameters
    ----------
        name (str) : name to search by

    Raises
    -------
        400 : Bad Request

    Returns
    -------
        Json ->
        {

            songs : [ SongDTOJson , ...]
            playlists : [ PlaylistDTOJson , ...]
            artists : [ ArtistJson , ... ]
            users : [ UserJson , ... ]

        }

    """

    if not checkValidParameterString(name):
        raise HTTPException(
            status_code=400, detail="El nombre por el que buscar es vacío"
        )

    items = {}

    try:
        songs = song_service.search_by_name(name)
        playlists = playlist_service.search_by_name(name)
        users = user_service.search_by_name(name)
        artists = artist_service.search_by_name(name)

        items["artistas"] = artists
        items["playlists"] = playlists
        items["users"] = users
        items["songs"] = songs

        return json.dumps(items)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"No se pudieron obtener los items por nombre | {e}"
        )
