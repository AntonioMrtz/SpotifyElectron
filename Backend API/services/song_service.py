import logging
import json
from database.Database import Database
from gridfs import GridFS
from bson import ObjectId
from fastapi import  HTTPException
from fastapi.responses import StreamingResponse



formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logging.basicConfig(level=logging.DEBUG)


""" Insert songs with format files,chunks https://www.mongodb.com/docs/manual/core/gridfs/"""
gridFsSong = GridFS(Database().connection, collection='cancion')



#TODO
""" Como devolver cancion mediante respuesta HTTP """
async def get_song(nombre : str):
    
    file = gridFsSong.get(ObjectId("64865b35c37038b371e94775")).read().decode('latin-1')

    print(type(file))
    return file
            
    #return StreamingResponse(file_data, media_type="audio/mpeg")

    

""" Nombre atrribute of song is his ID ( cannot be duplicate , checked on insert)"""
def create_song(nombre : str, artista : str,genero : str,file) -> str:

    

    if gridFsSong.find_one({"nombre":nombre}) is None:    

        file_id = gridFsSong.put(file, nombre=nombre,artista=artista,genero=genero)
        print(file_id)
        #return file_id
        return {"id":str(file_id)}

    raise HTTPException(status_code=400, detail="La canción no se pudo agregar o ya existía")