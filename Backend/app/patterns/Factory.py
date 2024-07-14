"""
Song Service Factory Pattern
"""

from abc import ABC, abstractmethod
from types import ModuleType


class BaseSongServiceModuleFactory(ABC):
    """Base factory for creating song services"""

    @abstractmethod
    def create_song_service(self) -> ModuleType:
        """Abstract method forcing creating a song service

        Returns:
            ModuleType: the song service module
        """
        pass
