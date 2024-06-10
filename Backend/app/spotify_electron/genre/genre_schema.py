"""
Genre schema for domain model
"""

from enum import StrEnum

from app.exceptions.base_exceptions_schema import SpotifyElectronException
from app.logging.logging_constants import LOGGING_GENRE_CLASS
from app.logging.logging_schema import SpotifyElectronLogger

genre_class_logger = SpotifyElectronLogger(LOGGING_GENRE_CLASS).getLogger()


class Genre(StrEnum):
    """Class to store the existing genres and their string representation"""

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
    def check_valid_genre(genre: str) -> bool:
        """Checks if the genre is valid and raises an exception if not"""
        if genre not in {member.value for member in Genre}:
            genre_class_logger.exception(f"Genre {genre} is not a valid Genre")
            raise GenreNotValidException
        return True

    @staticmethod
    def get_genre_string_value(genre: StrEnum) -> str:
        """Gets genre string representation value from Genre

        Args:
            genre (Enum): the genre Enum

        Raises:
            GenreNotValidException: if the genre doesn't match any existing genres

        Returns:
            str: the string representation of the genre
        """
        try:
            return str(genre.value)
        except Exception as exception:
            genre_class_logger.exception(f"Genre {genre} is not a valid Genre")
            raise GenreNotValidException from exception


class GenreNotValidException(SpotifyElectronException):
    """Exception for getting a Genre from an invalid value"""

    ERROR = "The genre doesnt exists"

    def __init__(self):
        super().__init__(self.ERROR)


class GenreServiceException(SpotifyElectronException):
    """Exception for unexpected error getting genres"""

    ERROR = "Unexpected error while getting genres"

    def __init__(self):
        super().__init__(self.ERROR)
