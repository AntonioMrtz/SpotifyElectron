import logging


class SpotifyElectronFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: (
            "%(asctime)s - %(name)s - \033[94m%(levelname)s\033[0m - %(message)s"
        ),
        logging.INFO: (
            "%(asctime)s - %(name)s - \033[92m%(levelname)s\033[0m - %(message)s"
        ),
        logging.WARNING: (
            "%(asctime)s - %(name)s - \033[93m%(levelname)s\033[0m - %(message)s"
        ),
        logging.ERROR: (
            "%(asctime)s - %(name)s - \033[91m%(levelname)s\033[0m - %(message)s"
        ),
        logging.CRITICAL: (
            "%(asctime)s - %(name)s - \033[95m%(levelname)s\033[0m - %(message)s"
        ),
    }

    def format(self, record):
        log_format = self.FORMATS.get(
            record.levelno, "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        formatter = logging.Formatter(log_format)
        return formatter.format(record)


class SpotifyElectronLogger:
    def __init__(self, logger_name, log_file=None):
        # Disable other loggers
        logging.getLogger().handlers.clear()
        logging.getLogger().propagate = False

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(
            logging.DEBUG
        )  # Set the logging level for this handler

        # Create a formatter
        console_formatter = SpotifyElectronFormatter()

        # Set the formatter for the console handler
        console_handler.setFormatter(console_formatter)

        # Add the console handler to the logger
        self.logger.addHandler(console_handler)

        # Create a file handler if log_file is provided
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(
                logging.ERROR
            )  # Set the logging level for this handler

            # Create a formatter for the file handler
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s \n"
            )

            # Set the formatter for the file handler
            file_handler.setFormatter(file_formatter)

            # Add the file handler to the logger
            self.logger.addHandler(file_handler)

    def getLogger(self):
        return self.logger
