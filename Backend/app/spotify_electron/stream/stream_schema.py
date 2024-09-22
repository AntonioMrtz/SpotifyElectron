"""
Stream schema for domain model
"""

from dataclasses import dataclass

from app.exceptions.base_exceptions_schema import SpotifyElectronException


@dataclass
class StreamAudioContent:
    """Content data for streaming audio"""

    start: int
    end: int
    headers: dict[str, str]
    song_data: bytes


class StreamServiceException(SpotifyElectronException):
    """Exception for Stream Service Unexpected Exceptions"""

    ERROR = "Error accessing Stream Service"

    def __init__(self):
        super().__init__(self.ERROR)


class InvalidContentRangeStreamException(SpotifyElectronException):
    """Exception for invalid content range provided for streaming"""

    ERROR = "Invalid content range for streaming"

    def __init__(self):
        super().__init__(self.ERROR)
