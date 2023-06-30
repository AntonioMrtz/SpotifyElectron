from dataclasses import dataclass

import services.song_service as song_service


@dataclass
class Playlist:

    name: str
    photo : str
    songs : list

    """ @property
    def get_number_songs():

        return len(getattr(song_names)) """

    def add_songs(song_names : str )-> None:

        [ songs.append(song_service.get_song(song_name)) for song_name in song_names]