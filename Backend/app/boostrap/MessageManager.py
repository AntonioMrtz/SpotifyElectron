import configparser


class MessageConfig:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        # Dynamically set attributes for each message
        for key, value in self.config["messages"].items():
            setattr(self, key, value)


# Example usage:
if __name__ == "__main__":
    config_file = "config.ini"
    message_config = MessageConfig(config_file)

    # Access messages as attributes
    print("Welcome Message:", message_config.welcome_message)
    print("Error Message:", message_config.error_message)
