import socket
import configparser
import os
import time
from message_codecs import *
from tests.logger import Logger  # Import the custom logger

# Instantiate the logger
logger = Logger().get_logger()

class MessageSender:
    state_duration = 100  # milliseconds

    @staticmethod
    def send_message(message):
        from gui.graph import Graph  # Move import here to avoid circular import

        config = configparser.ConfigParser()
        script_dir = os.path.dirname(__file__)
        config_path = os.path.join(script_dir, 'config.ini')

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        config.read(config_path)

        if 'server' not in config:
            raise KeyError("The 'server' section is missing in the config file.")

        host = config['server']['host']
        port = int(config['server']['port'])

        logger.info(f"Message to send: {message}")
        binary_message = BinaryConverter.utf8_to_binary(message)
        logger.debug(f"Binary message: {binary_message}")
        encrypted_message = XORCipher.encrypt(binary_message)
        logger.debug(f"Encrypted message: {encrypted_message}")
        signal = LineCode2B1Q.apply_2b1q(encrypted_message)
        logger.debug(f"Signal: {signal}")

        # Return the details as a JSON object
        return {
            "status": "Ready to Send",
            "raw_message": message,
            "binary_message": binary_message,
            "encrypted_message": encrypted_message,
            "encoded_message": signal
        }

    @staticmethod
    def send_signal(signal):
        config = configparser.ConfigParser()
        script_dir = os.path.dirname(__file__)
        config_path = os.path.join(script_dir, 'config.ini')

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        config.read(config_path)

        if 'server' not in config:
            raise KeyError("The 'server' section is missing in the config file.")

        host = config['server']['host']
        port = int(config['server']['port'])

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            for value in signal:
                s.sendall(bytes([int(value) + 128]))
                logger.debug(f"Sent value: {value}")
                time.sleep(MessageSender.state_duration / 1000)  # Send each value with delay