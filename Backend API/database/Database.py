from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import logging
from dotenv import load_dotenv


formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logging.basicConfig(level=logging.WARNING)

load_dotenv()

""" Singleton instance of the MongoDb connection """
class Database():

    """ Direct connection to the MongoDB client """
    connection = None
    """ Connection to the list database """
    list_collection = None
    """ Connection to the song database """
    song_collection = None


    def __init__(self):
      if Database.connection is None:
         try:

            
            password = os.getenv("MONGO_PASS")
            uri = 'mongodb+srv://arso:'+str(password)+'@cluster0.ktobcwq.mongodb.net/?retryWrites=true&w=majority'
            Database.connection = MongoClient(uri, server_api=ServerApi('1'))["SpotifyElectron"]
            Database.list_collection = Database.connection["list"]
            Database.song_collection = Database.connection["song"]


         except Exception as error:
            logging.warning("Error: Connection not established {}".format(error))
         else:
            logging.info("Connection established")

      connection = Database.connection
      song_collection =  Database.song_collection
      list_collection = Database.list_collection


