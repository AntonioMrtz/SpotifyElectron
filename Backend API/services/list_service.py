from database.Database import Database
import logging
import json

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logging.basicConfig(level=logging.DEBUG)


def hola():
    print("gola")