from app.exceptions.exceptions_schema import SpotifyElectronException


class DatabasePingFailed(SpotifyElectronException):
    """Exception for database ping failure"""

    ERROR = "Ping to the database failed"

    def __init__(self):
        super().__init__(self.ERROR)


class UnexpectedDatabasePingFailed(SpotifyElectronException):
    """Exception for unexpected database ping failure"""

    ERROR = "Unexpected error while pinging to the database"

    def __init__(self, exception: Exception):
        super().__init__(f"{self.ERROR} : {exception}")
