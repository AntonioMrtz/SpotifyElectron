
from fastapi import HTTPException

from app.model.DTO.SongDTO import SongDTO
from app.model.Genre import Genre
from app.services.song_services.song_service_provider import get_song_service
from app.services.utils import checkValidParameterString

song_service = get_song_service()


def get_song(name: str) -> SongDTO:
    """Returns a song's metadata without his audio file"

    Parameters
    ----------
        name (str) : name of the song

    Raises
    -------
        400 : Bad Request
        404 : Song not found

    Returns
    -------
        SongDTO
    """
    if not checkValidParameterString(name):
        raise HTTPException(status_code=400, detail="El nombre de la canción es vacío")

    song = song_service.get_song(name)
    if song is None:
        raise HTTPException(
            status_code=404, detail="La canción con ese nombre no existe"
        )

    return SongDTO(
        name=song.name,
        artist=song.artist,
        photo=song.photo,
        seconds_duration=song.seconds_duration,
        genre=song.genre,
        number_of_plays=song.number_of_plays,
    )


def get_songs(song_names: list) -> list:
    """Returns a list with song's metadatas without his audio files"

    Parameters
    ----------
        song_names (list) : song names

    Raises
    -------
        400 : Bad Request
        404 : Song not found

    Returns
    -------
        List<SongDTO>
    """
    # TODO , request all songs in the same query

    respone_songs_dto = []

    for name in song_names:
        if not checkValidParameterString(name):
            raise HTTPException(
                status_code=400, detail="El nombre de la canción es vacío"
            )

        song_data = song_service.get_song(name)
        if song_data is None:
            raise HTTPException(
                status_code=404, detail="La canción con ese nombre no existe"
            )

        respone_songs_dto.append(song_data)

    return respone_songs_dto


def get_songs_by_genero(genre: Genre) -> list[SongDTO]:
    """Increase the number of plays of a song

    Parameters
    ----------
        name (str): Song's name

    Raises
    -------
        400 : Bad Request
        404 : Song Not Found

    Returns
    -------
    List<Song>

    """

    if not checkValidParameterString(genre.value):
        raise HTTPException(status_code=400, detail="Parámetros no válidos")

    if not Genre.check_valid_genre(genre.value):
        raise HTTPException(status_code=404, detail="El género no existe")

    songs_by_genre = song_service.get_songs_by_genre(genre)
    songs_dto_by_genre = []

    for song in songs_by_genre:
        songs_dto_by_genre.append(
            SongDTO(
                name=song.name,
                artist=song.artist,
                photo=song.photo,
                seconds_duration=song.seconds_duration,
                genre=song.genre,
                number_of_plays=song.number_of_plays,
            )
        )

    return songs_dto_by_genre


# TODO create method to transform from song to song dto
