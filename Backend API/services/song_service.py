import logging
import json
from database.Database import Database
from gridfs import GridFS

from fastapi import  HTTPException



formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logging.basicConfig(level=logging.DEBUG)

""" Insert songs with format files,chunks https://www.mongodb.com/docs/manual/core/gridfs/"""
gridFsSong = GridFS(Database().connection, collection='cancion')

list_collection = Database().list_collection
song_files_collection = Database().song_collection


def get_song(nombre : str):
    

    

    file_id = gridFsSong.put(file, nombre=nombre,artista=artista,genero=genero)
    print('Archivo MP3 almacenado con éxito. ID del archivo:', file_id)

""" Nombre atrribute of song is his ID ( cannot be duplicate , checked on insert)"""
def create_song(nombre : str, artista : str,genero : str,file) -> str:

    

    if gridFsSong.find_one({"nombre":nombre}) is None:    

        file_id = gridFsSong.put(file, nombre=nombre,artista=artista,genero=genero)
        return file_id

    raise HTTPException(status_code=400, detail="La canción no se pudo agregar o ya existía")