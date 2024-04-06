from app.exceptions.exceptions_schema import SpotifyElectronException


class ServiceException(SpotifyElectronException):
    """Exception for Repository Exceptions"""

    def __init__(self, service_name: str):
        self._set_service_name(service_name)
        super().__init__(self.error)

    def _set_service_name(self, repository_name: str):
        self.error = f"Error in {repository_name} Service"


class BadParameterException(SpotifyElectronException):
    """Exception for bad parameter"""

    def __init__(self, parameter_name: str):
        self._set_parameter_name(parameter_name)
        super().__init__(self.error)

    def _set_parameter_name(self, item_name: str):
        self.error = f"Bad parameter : {item_name}"


class UnAuthorizedException(SpotifyElectronException):
    """Exception for user accesing unauthorized resource"""

    def __init__(self, user: str):
        super().__init__(self.error)

    def _set_user_name(self, user: str):
        self.error = f"Unauthorized user : {user}"
