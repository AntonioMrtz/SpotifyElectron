from model.DTO.SongDTO import SongDTO
from model.DTO.PlaylistDTO import PlaylistDTO
from database.Database import Database
from model.Genre import Genre
from fastapi import HTTPException


fileSongCollection = Database().connection["cancion.files"]
playlistCollection = Database().connection["playlist"]


def get_song(name: str) -> SongDTO:
    """ Returns a song's metadata without his audio file"

    Args:
        name (str) : name of the song

    Raises:
        400 : Bad Request
        404 : Song not found

    Returns:
        SongDTO
    """
    if name is None or name == "":
        raise HTTPException(
            status_code=400, detail="El nombre de la canción es vacío")

    song_data = fileSongCollection.find_one({'name': name})
    if song_data is None:
        raise HTTPException(
            status_code=404, detail="La canción con ese nombre no existe")

    return SongDTO(name=song_data["name"], artist=song_data["artist"], photo=song_data["photo"], duration=song_data["duration"],genre=Genre(song_data["genre"]).name)


def get_playlist(name: str) -> PlaylistDTO:
    """ Returns a playlist's metadata without his song's audio files"

    Args:
        name (str) : name of the playlist

    Raises:
        400 : Bad Request
        404 : Playlist not found

    Returns:
        PlaylistDTO
    """

    if name is None or name == "":
        raise HTTPException(
            status_code=400, detail="El nombre de la playlist es vacío")

    playlist_data = playlistCollection.find_one({'name': name})

    if playlist_data is None:
        raise HTTPException(
            status_code=404, detail="La playlist con ese nombre no existe")

    return PlaylistDTO(name=playlist_data["name"], photo=playlist_data["photo"], song_names=playlist_data["song_names"])
