from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logging.basicConfig(level=logging.WARNING)

load_dotenv()

""" Singleton instance of the MongoDb connection """


class DatabaseMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=DatabaseMeta):

    """ Direct connection to the MongoDB client """
    connection = None
    """ Connection to the list database """
    list_collection = None
    """ Connection to the song database """
    song_collection = None

    def __init__(self):
        if Database.connection is None:
            try:
                password = os.getenv("MONGO_PASSWORD")
                uri = 'mongodb+srv://arso:' + \
                    str(password) + \
                    '@cluster0.ktobcwq.mongodb.net/?retryWrites=true&w=majority'
                Database.connection = MongoClient(uri, server_api=ServerApi('1'))[
                    "SpotifyElectron"]
                Database.list_collection = Database.connection["playlist"]
                Database.song_collection = Database.connection["song"]

            except Exception as error:
                logging.warning(
                    "Error: Connection not established {}".format(error))
            else:
                logging.info("Connection established")
