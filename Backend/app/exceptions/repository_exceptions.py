from app.exceptions.exceptions_schema import SpotifyElectronException


class RepositoryException(SpotifyElectronException):
    """Exception for Repository Exceptions"""

    def __init__(self, repository_name: str):
        self._set_repository_name(repository_name)
        super().__init__(self.error)

    def _set_repository_name(self, repository_name: str):
        self.error = f"Error accesing {repository_name} Repository"


class ItemNotFoundException(SpotifyElectronException):
    """Exception for item not found"""

    def __init__(self, item_name: str):
        self._set_item_name(item_name)
        super().__init__(self.error)

    def _set_item_name(self, item_name: str):
        self.error = f"Item {item_name} not found"
