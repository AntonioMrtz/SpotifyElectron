"""TODO"""

import asyncio
import json

from ..__main__ import app, lifespan_handler

OPENAPI_SCHEMA_OUTPUT_FILE = "app/resources/openapi.json"


async def generate_openapi() -> None:
    """Generates OpenAPI schema and writes it into a file"""
    async with lifespan_handler(app):
        print("> Generating OpenAPI Schema")
        openapi = app.openapi()
        openapi_json = json.dumps(openapi, indent=2)
        with open(OPENAPI_SCHEMA_OUTPUT_FILE, "w") as file:
            print(f"> Writing OpenAPI Schema on {OPENAPI_SCHEMA_OUTPUT_FILE}")
            file.write(openapi_json)


if __name__ == "__main__":
    asyncio.run(generate_openapi())
