from fastapi.testclient import TestClient
import logging

from main import app as app

client = TestClient(app)




