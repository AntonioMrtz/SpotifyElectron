def checkValidParameterString(parameter: str) -> bool:
    """ Checks if the parameter string is not None or empty"""
    if parameter == None or parameter == "":
        return False

    return True
