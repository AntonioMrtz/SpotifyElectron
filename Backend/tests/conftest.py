import os
from fastapi.testclient import TestClient
from pytest import fixture
from app.__main__ import app


@fixture(scope="module")
def trigger_app_start():
    with TestClient(app):
        yield


@fixture(scope="function")
def clean_modified_environments():
    original_env = dict(os.environ)
    yield
    for key in os.environ.keys():
        if key not in original_env:
            del os.environ[key]
        elif os.environ[key] != original_env[key]:
            os.environ[key] = original_env[key]
