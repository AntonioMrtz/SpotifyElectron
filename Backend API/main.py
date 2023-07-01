from fastapi import FastAPI, UploadFile, status
import services.song_service as song_service
import services.playlist_service as playlist_service
import services.dto_service as dto_service
from fastapi.responses import Response
import json
from model.Genre import Genre
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="SpotifyElectronAPI",
              description="API created with FastAPI Python to serve as backend for SpotifyElectron App",
              version="0.0.1"

              )
""" Cors disabled """
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
  		allow_headers=["*"],
    max_age=3600,
)

#* CANCIONES

@app.get("/canciones/{nombre}")
def get_cancion(nombre: str) -> Response:
    """ Devuelve la canción con nombre "nombre"

    Args:
        nombre (str): Nombre de la canción

    Returns:
        Response 200 OK

    Raises:
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe una canción con el nombre "nombre"
    """

    song = song_service.get_song(nombre)
    song_json = song.get_json()

    return Response(song_json, media_type="application/json", status_code=200)


@app.post("/canciones/")
async def post_cancion(nombre: str, artista: str, genero: Genre, foto: str, file: UploadFile) -> Response:
    """ Registra la canción con los parámetros "nombre","artista" y "género"

    Args:
        nombre (str): Nombre de la canción
        artista (str): Artista de la canción
        genero (Genre): Género musical de la canción
        foto (url): Género musical de la canción


    Returns:
        Response 201 Created

    Raises:
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
    """

    readFile = await file.read()
    song_service.create_song(nombre, artista, genero, foto, readFile)
    return Response(None, 201)


@app.get("/canciones/")
def get_canciones() -> Response:
    """ Devuelve todas las canciones

    Args:

    Returns:
        Response 200 OK

    Raises:
    """

    songs = song_service.get_songs()

    songs_list = []
    [songs_list.append(song.get_json()) for song in songs]

    songs_dict = {}

    songs_dict["songs"] = songs_list
    songs_json = json.dumps(songs_dict)

    return Response(songs_json, media_type="application/json", status_code=200)

#* PLAYLISTS

@app.get("/playlists/{nombre}")
def get_lista(nombre: str) -> Response:
    """ Devuelve la playlist con nombre "nombre"

    Args:
        nombre (str): Nombre de la playlist

    Returns:
        Response 200 OK

    Raises:
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe una playlist con el nombre "nombre"
    """

    playlist = playlist_service.get_playlist(nombre)

    playlist_json = playlist.get_json()

    return Response(playlist_json, media_type="application/json", status_code=200)


@app.post("/playlists/")
def post_playlist(nombre: str, foto: str, nombres_canciones: list) -> Response:
    """ Registra la canción con los parámetros "nombre","artista" y "género"

    Args:
        nombre (str): Nombre de la playlist
        foto (url): Género musical de la canción
        nombres_canciones (list) : nombres de las canciones


    Returns:
        Response 201 Created

    Raises:
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
    """

    result = playlist_service.create_playlist(nombre, foto, nombres_canciones)
    return Response(None, 201)


@app.put("/playlists/{nombre}")
def update_playlist(nombre: str, nombres_canciones: list, foto: str = "") -> Response:
    """ Actualiza los parámetros de la playlist con nombre "nombre""

    Args:
        nombre (str): Nombre de la playlist
        nombres_canciones (list) : Lista con las canciones de la playlist
        foto (str) : url de la foto miniatura de la playlist

    Returns:
        Response 204 No content

    Raises:
        Bad Request 400: Parámetros introducidos no són válidos o vacíos
        Not Found 404: No existe una playlist con el nombre "nombre"
    """

    playlist_service.update_playlist(nombre, foto, nombres_canciones)
    return Response(None, 204)

#* DTO
""" Objects with only the data the user needs to visualize """


@app.get("/canciones/dto/{nombre}")
def get_cancion_dto(nombre: str) -> Response:
    """ Devuelve la canción con nombre "nombre" con los dato necesarios para previsualizacion sin carga el contenido de la canción

    Args:
        nombre (str): Nombre de la canción

    Returns:
        Response 200 OK

    Raises:
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe una canción con el nombre "nombre"
    """

    song = dto_service.get_song(nombre)
    song_json = song.get_json()

    return Response(song_json, media_type="application/json", status_code=200)


@app.get("/playlists/dto/{nombre}")
def get_lista_dto(nombre: str) -> Response:
    """ Devuelve la playlist con nombre "nombre" con los datos necesarios para previsualización , sin el contenido de las canciones

    Args:
        nombre (str): Nombre de la playlist

    Returns:
        Response 200 OK

    Raises:
        Bad Request 400: "nombre" es vacío o nulo
        Not Found 404: No existe una playlist con el nombre "nombre"
    """

    playlist = dto_service.get_playlist(nombre)
    playlist_json = playlist.get_json()

    return Response(playlist_json, media_type="application/json", status_code=200)


@app.get("/generos/")
def get_generos() -> Response:

    genres = song_service.get_genres()

    return Response(genres, media_type="application/json", status_code=200)
