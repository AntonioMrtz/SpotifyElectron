from model.DTO.SongDTO import SongDTO
from model.DTO.PlaylistDTO import PlaylistDTO
from database.Database import Database
from model.Genre import Genre

fileSongCollection = Database().connection["cancion.files"]
playlistCollection = Database().connection["playlist"]


def get_song(name: str) -> SongDTO:

    if name is None or name == "":
        raise HTTPException(
            status_code=400, detail="El nombre de la canción es vacío")

    song_data = fileSongCollection.find_one({'name': name})
    if song_data is None:
        raise HTTPException(
            status_code=404, detail="La canción con ese nombre no existe")

    return SongDTO(name=song_data["name"], artist=song_data["artist"], photo=song_data["photo"], genre=Genre(song_data["genre"]).name)


def get_playlist(name: str) -> SongDTO:

    playlist_data = playlistCollection.find_one({'name': name})

    return PlaylistDTO(name=playlist_data["name"], photo=playlist_data["photo"], song_names=playlist_data["song_names"])
