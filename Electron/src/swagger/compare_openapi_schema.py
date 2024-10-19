"""Script for comparing two OpenAPI schemas

Params:
    first_openapi_schema_path
    second_openapi_schema_path

Example:
    python openapi.json other-openapi.json

Return:
    0 - OpenAPI schemas are equal
    1 - OpenAPI schemas are different
"""

import sys


def compare_openapi_schema(first_path: str, second_path: str) -> None:
    """Compare two OpenAPI schemas

    Args:
        first_path (str): first openapi file path
        second_path (str): second openapi file path
    """
    with (
        open(first_path, "rb") as old_openapi_schema,
        open(second_path, "rb") as new_openapi_schema,
    ):
        if old_openapi_schema.read() == new_openapi_schema.read():
            sys.exit(0)

    sys.exit("OpenAPI schemas are different")


if __name__ == "__main__":
    EXPECTED_ARGS = 3
    assert len(sys.argv) >= EXPECTED_ARGS

    print(
        f"> Executing {sys.argv[0]} with OpenAPI Schemas {sys.argv[1]} and {sys.argv[2]}"
    )

    first_openapi_schema_path = sys.argv[1]
    second_openapi_schema_path = sys.argv[2]
    compare_openapi_schema(first_openapi_schema_path, second_openapi_schema_path)
