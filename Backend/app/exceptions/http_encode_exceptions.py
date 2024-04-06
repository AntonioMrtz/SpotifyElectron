from app.exceptions.exceptions_schema import SpotifyElectronException


class JsonEncodeException(SpotifyElectronException):
    """Exception for error encoding object into json"""

    ERROR = "Error encoding object into json"

    def __init__(self):
        super().__init__(self.ERROR)
