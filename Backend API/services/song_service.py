from database.Database import Database
import logging
import json

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logging.basicConfig(level=logging.DEBUG)


list_collection = Database().list_collection

def create_song():
    prueba = {"hola" : "si"}

    list_collection.insert_one(prueba)
    