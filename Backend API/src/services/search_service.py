from services.utils import checkValidParameterString
from fastapi import HTTPException
import services.song_service as song_service
import services.playlist_service as playlist_service
import services.user_service as user_service
import services.artist_service as artist_service
import json


def search_by_name(name: str) -> json:
    """ Returns songs, artist and playlist that matches name

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
            status_code=400, detail="El nombre por el que buscar es vacío")

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
            status_code=500, detail=f"No se pudieron obtener los items por nombre | {e}")
