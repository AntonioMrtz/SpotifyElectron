import json

from app.genre.genre_schema import Genre, GenreServiceException
from app.logging.logger_constants import LOGGING_GENRE_SERVICE
from app.logging.logging_schema import SpotifyElectronLogger

genre_service_logger = SpotifyElectronLogger(LOGGING_GENRE_SERVICE).getLogger()


def get_genres() -> str:
    """Returns a json with all the available genres

    Raises:
        UnexpectedGenreServiceError: if an unexpected error occurred

    Returns:
        str: _description_
    """
    try:
        genre_dict = {}
        for genre in Genre:
            genre_dict[genre.name] = genre.value
        genres_json = json.dumps(genre_dict)
    except Exception as exception:
        genre_service_logger.exception("Unhandled error getting genres")
        raise GenreServiceException from exception
    else:
        genre_service_logger.info(f"Obtained genres : {genres_json}")
        return genres_json