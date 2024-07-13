"""Generate OpenAPI Schema from app

Steps:
    1. Go to Backend/
    2. Run `python -m app.tools.generate_openapi`
    3. OpenAPI Schema will be located at OPENAPI_SCHEMA_OUTPUT_FILE path
"""

import asyncio
import json
import os

from app.__main__ import app, lifespan_handler

OPENAPI_SCHEMA_OUTPUT_FOLDER = "../Electron/src/swagger/"
OPENAPI_SCHEMA_OUTPUT_FILE = f"{OPENAPI_SCHEMA_OUTPUT_FOLDER}openapi.json"


def check_openapi_folder_exists() -> bool:
    """Checks if folder that has to store OpenAPI file exists

    Returns:
    -------
        bool: if the OpenAPI folder exists
    """
    cwd = os.path.abspath(os.getcwd())
    print(f"> Current Working Directory: {cwd}")
    openapi_expected_path_folder = os.path.join(
        os.path.abspath(os.getcwd()), OPENAPI_SCHEMA_OUTPUT_FOLDER
    )
    print(f"> Checking if {openapi_expected_path_folder} folder exists")
    if not os.path.exists(openapi_expected_path_folder):
        print(f"> Folder {openapi_expected_path_folder} doesnt exists")
        return False
    print(f"> Folder {openapi_expected_path_folder} exists")
    return True


async def generate_openapi() -> None:
    """Generates OpenAPI schema and writes it into a file"""
    if not check_openapi_folder_exists():
        return
    async with lifespan_handler(app):
        print("> Generating OpenAPI Schema")
        openapi = app.openapi()
        openapi_json = json.dumps(openapi, indent=2)
        with open(OPENAPI_SCHEMA_OUTPUT_FILE, "w") as file:
            print(f"> Writing OpenAPI Schema on {OPENAPI_SCHEMA_OUTPUT_FILE}")
            file.write(openapi_json)


if __name__ == "__main__":
    asyncio.run(generate_openapi())
