from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os


class Database():

    connection = None
    list_collection = None
    song_collection = None


    def __init__(self):
      if Database.connection is None:
         try:

            password = os.getenv("MONGO_PASS")
            uri = f'mongodb+srv://arso:{password}@cluster0.ktobcwq.mongodb.net/?retryWrites=true&w=majority'
            Database.connection = MongoClient(uri, server_api=ServerApi('1'))
            Database.collection_list = Database.connection["list"]
            Database.collection_song = Database.connection["song"]


         except Exception as error:
            print("Error: Connection not established {}".format(error))
         else:
            print("Connection established")

      self.connection = Database.connection
      self.collection_cancion =  Database.collection_song
      self.collection_list = Database.collection_list


