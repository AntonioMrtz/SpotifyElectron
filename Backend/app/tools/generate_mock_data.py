"""Generate mock data

Commands:
    help: print script usage
    small|medium|large: the size of the mock data

Steps:
    1. Go to Backend/
    2. Run `python -m app.tools.generate_mock_data [(help) | (small|medium|large)]`
"""

import asyncio
import sys
from enum import StrEnum

from app.__main__ import app, lifespan_handler
from tests.test_API.api_test_artist import create_artist
from tests.test_API.api_test_playlist import create_playlist
from tests.test_API.api_test_song import create_song
from tests.test_API.api_test_user import create_user
from tests.test_API.api_token import get_user_jwt_header

HELP_COMMAND = "help"


class DataSize(StrEnum):
    SMALL_MOCK_DATA_COMMAND = "small"
    MEDIUM_MOCK_DATA_COMMAND = "medium"
    LARGE_MOCK_DATA_COMMAND = "large"


amout_items_per_data_size: dict[DataSize | str, int] = {
    DataSize.SMALL_MOCK_DATA_COMMAND: 20,
    DataSize.MEDIUM_MOCK_DATA_COMMAND: 100,
    DataSize.MEDIUM_MOCK_DATA_COMMAND: 500,
}


async def generate_mock_data(size: str) -> None:
    """Generates mock data

    Args:
        size (str): the size of the data to generate. Check `DataSize`
    """
    amout_items = amout_items_per_data_size.get(
        size, amout_items_per_data_size[DataSize.SMALL_MOCK_DATA_COMMAND]
    )
    async with lifespan_handler(app):
        for i in range(0, amout_items):
            create_user(f"item-user{i}", "", "password")
            jwt_headers_user = get_user_jwt_header(
                username=f"item-user{i}", password="password"
            )
            for j in range(0, int(amout_items / 10)):
                create_playlist(
                    f"item-playlist{j}-user{i}", "description", "", jwt_headers_user
                )
            create_artist(f"item-artist{i}", "", "password")
            jwt_headers_artist = get_user_jwt_header(
                username=f"item-artist{i}", password="password"
            )
            for j in range(0, int(amout_items / 10)):
                create_playlist(
                    f"item-playlist{j}-artist{i}", "description", "", jwt_headers_user
                )
                create_song(
                    f"item-song{j}-artist{i}",
                    "tests/assets/song_4_seconds.mp3",
                    "Pop",
                    "",
                    jwt_headers_artist,
                )


def print_help():
    """Prints script usage"""
    print(
        "----------------------------\n"
        "Commands\n\n"
        "help: print script usage\n"
        "small|medium|large: the size of the mock data\n"
        "----------------------------\n"
    )


def main() -> None:
    """Handles the script's command-line interface."""
    if len(sys.argv) <= 1:
        print("Invalid options. Use help command")
        return

    command = sys.argv[1]

    if command == HELP_COMMAND:
        print_help()
        return

    if command in DataSize.__members__.values():
        asyncio.run(generate_mock_data(command))
        return

    print("Invalid command. Use --help")


if __name__ == "__main__":
    main()
