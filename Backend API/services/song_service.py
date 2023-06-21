import logging
from services.utils import checkValidParameterString
from database.Database import Database
from gridfs import GridFS
from bson import ObjectId
from fastapi import HTTPException
from fastapi.responses import Response
from model.Genre import Genre

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logging.basicConfig(level=logging.DEBUG)

""" Insert songs with format [files,chunks] https://www.mongodb.com/docs/manual/core/gridfs/"""
gridFsSong = GridFS(Database().connection, collection='cancion')


def get_song(nombre: str) -> Response:

    if nombre is None or nombre == "":
        raise HTTPException(
            status_code=400, detail="El nombre de la canción es vacío")

    song_bytes = gridFsSong.find_one({'nombre': nombre})

    if song_bytes is None:
        raise HTTPException(
            status_code=404, detail="La canción con ese nombre no existe")

    return Response(song_bytes.read(), media_type="audio/mp3", status_code=200)


def create_song(nombre: str, artista: str, genero: Genre, foto: str, file) -> Response:

    if not checkValidParameterString(nombre) or not checkValidParameterString(nombre) or not checkValidParameterString(nombre) or not Genre.checkValidGenre(genero.value):
        raise HTTPException(
            status_code=400, detail="Parámetros no válidos o vacíos")

    if gridFsSong.exists({"nombre": nombre}):
        raise HTTPException(status_code=400, detail="La canción ya existe")

    file_id = gridFsSong.put(
        file, nombre=nombre, artista=artista, genero=str(genero.value), foto=foto)
    return Response(None, 201)
