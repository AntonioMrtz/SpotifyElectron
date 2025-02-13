import os

from fastapi.testclient import TestClient
from pytest import fixture


@fixture(scope="module")
def trigger_app_startup():
    """Forces FASTAPI app startup event"""
    print("\nCurrent environment variables:")
    for key, value in os.environ.items():
        if key in {"MONGO_URI", "ENV_VALUE", "ARCH"}:
            print(f"{key}: {value}")

    from app.__main__ import app

    with TestClient(app):
        yield


@fixture(scope="function")
def clean_modified_environments():
    """Stores environment variables present before function execution and restores them\
     after function execution took place
    """
    original_env = dict(os.environ)
    yield
    for key in os.environ:
        if key not in original_env:
            del os.environ[key]
        elif os.environ[key] != original_env[key]:
            os.environ[key] = original_env[key]
