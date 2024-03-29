from abc import ABC, abstractmethod


class SpotifyElectronModel(ABC):
    """Abstract Base Model"""

    @abstractmethod
    def get_json() -> str:
        """Returns the object as json string

        Returns:
            str: the object as json strin
        """
        pass
