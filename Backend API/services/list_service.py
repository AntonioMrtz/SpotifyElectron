from database.Database import Database
import logging
import json

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logging.basicConfig(level=logging.DEBUG)

list_collection = Database.get_list_collection
song_files_collection = Database.get_song_collection



def hola():
    print("gola")