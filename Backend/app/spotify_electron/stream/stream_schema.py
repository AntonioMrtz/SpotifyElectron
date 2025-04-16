"""Stream schema for domain model"""

from dataclasses import dataclass

from app.exceptions.base_exceptions_schema import SpotifyElectronError


@dataclass
class StreamAudioContent:
    """Content data for streaming audio"""

    start: int
    """Request start byte"""
    end: int
    """Request end byte"""
    headers: dict[str, str]
    """Response headers"""
    song_data: bytes
    """Song data from start-end bytes"""


class StreamServiceError(SpotifyElectronError):
    """Exception for Stream Service Unexpected Exceptions"""

    ERROR = "Error accessing Stream Service"

    def __init__(self):
        super().__init__(self.ERROR)


class InvalidContentRangeStreamError(SpotifyElectronError):
    """Exception for invalid content range provided for streaming"""

    ERROR = "Invalid content range for streaming"

    def __init__(self):
        super().__init__(self.ERROR)
