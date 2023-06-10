from database.Database import Database
import logging
import json

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logging.basicConfig(level=logging.DEBUG)

song_collection = Database().song_collection



def hola():
    print("gola")