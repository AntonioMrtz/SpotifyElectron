"""
Song Service Factory Pattern
"""

from abc import ABC, abstractmethod


class BaseSongServiceModuleFactory(ABC):
    """Base factory for creating song services"""

    @abstractmethod
    def create_song_service(self):
        """Abstract method forcing creating a song service"""
        pass
