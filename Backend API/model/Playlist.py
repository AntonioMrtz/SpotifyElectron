from dataclasses import dataclass

import services.song_service as song_service
import json


@dataclass
class Playlist:

    name: str
    photo: str
    songs: list

    def add_songs(song_names: str) -> None:

        [songs.append(song_service.get_song(song_name))
         for song_name in song_names]

    def get_json(self) -> json:

        playlist_dict = self.__dict__

        songs_json = []

        for song in self.songs:
            song_json = json.dumps(song.__dict__)
            songs_json.append(song_json)

        # Eliminar el atributo song_names del diccionario , hay que serializar song primero
        playlist_dict.pop('songs', None)
        # Convertir el diccionario en una cadena JSON
        playlist_dict['songs'] = songs_json
        playlist_json = json.dumps(playlist_dict)

        return playlist_json
