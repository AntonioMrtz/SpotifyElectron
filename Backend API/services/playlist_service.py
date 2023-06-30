from database.Database import Database
import services.song_service as song_service
from model.Playlist import Playlist
from model.Song import Song
from fastapi import HTTPException
import json

playlistCollection = Database().connection["playlist"]


def get_playlist(name : str) -> Playlist:
    
    playlist_data = playlistCollection.find_one({'name':name})

    if playlist_data is None:
        raise HTTPException(
            status_code=404, detail="La playlist con ese nombre no existe")

    playlist_songs = []

    [playlist_songs.append(song_service.get_song(song_name)) for song_name in playlist_data["song_names"]]

    #[print(song.name) for song in playlist_songs]

    playlist = Playlist(name,playlist_data["photo"],playlist_songs)

    return playlist

    

    


def create_playlist(name : str , photo : str , song_names : list):

    songs = song_service.get_songs(song_names)
    playlist = Playlist(name=name, photo=photo, songs=songs)

    result_playlist_exists = playlistCollection.find_one({'name':name})

    if result_playlist_exists:
        raise HTTPException(status_code=400, detail="La playlist ya existe")



    result = playlistCollection.insert_one({'name':name,'photo':photo,'song_names':song_names})

    return True if result.acknowledged else False

     