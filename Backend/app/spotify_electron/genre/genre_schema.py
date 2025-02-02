"""
Genre schema for domain model
"""

from enum import StrEnum

from app.exceptions.base_exceptions_schema import SpotifyElectronError
from app.logging.logging_constants import LOGGING_GENRE_CLASS
from app.logging.logging_schema import SpotifyElectronLogger

genre_class_logger = SpotifyElectronLogger(LOGGING_GENRE_CLASS).get_logger()


class Genre(StrEnum):
    """Song genres"""

    POP = "Pop"
    ROCK = "Rock"
    HIP_HOP = "Hip-hop"
    RNB = "R&B (Ritmo y Blues)"
    JAZZ = "Jazz"
    BLUES = "Blues"
    REGGAE = "Reggae"
    COUNTRY = "Country"
    FOLK = "Folk"
    CLASICA = "Clásica"
    ELECTRONICA = "Electrónica"
    DANCE = "Dance"
    METAL = "Metal"
    PUNK = "Punk"
    FUNK = "Funk"
    SOUL = "Soul"
    GOSPEL = "Gospel"
    LATIN = "Latina"
    WORLD_MUSIC = "Música del mundo"
    EXPERIMENTAL = "Experimental"
    AMBIENT = "Ambiental"
    FUSION = "Fusión"
    INSTRUMENTAL = "Instrumental"
    ALTERNATIVE = "Alternativa"
    INDIE = "Indie"
    RAP = "Rap"
    SKA = "Ska"
    GRUNGE = "Grunge"
    TRAP = "Trap"
    REGGAETON = "Reggaeton"

    @staticmethod
    def validate_genre(genre: str) -> None:
        """Checks if the genre is valid and raises an exception if not

        Args:
            genre (str): genre

        Raises:
            GenreNotValidError: invalid genre provided
        """
        if genre not in {member.value for member in Genre}:
            genre_class_logger.exception(f"Genre {genre} is not a valid Genre")
            raise GenreNotValidError

    @staticmethod
    def get_genre_string_value(genre: StrEnum) -> str:
        """Gets genre string representation value from Genre

        Args:
            genre (Enum): the genre Enum

        Raises:
            GenreNotValidError: if the genre doesn't match any existing genres

        Returns:
            str: the string representation of the genre
        """
        try:
            return str(genre.value)
        except Exception as exception:
            genre_class_logger.exception(f"Genre {genre} is not a valid Genre")
            raise GenreNotValidError from exception


class GenreNotValidError(SpotifyElectronError):
    """Getting a Genre from an invalid value"""

    ERROR = "The genre doesn't exists"

    def __init__(self):
        super().__init__(self.ERROR)


class GenreServiceError(SpotifyElectronError):
    """Unexpected error getting genres"""

    ERROR = "Unexpected error while getting genres"

    def __init__(self):
        super().__init__(self.ERROR)
