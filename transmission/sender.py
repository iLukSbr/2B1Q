import socket
import configparser
import os
from message_codecs import *

class MessageSender:
    state_duration = 500  # milliseconds

    @staticmethod
    def send_message(message):
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

        binary_message = BinaryConverter.utf8_to_binary(message)
        print(f"Binary message: {binary_message}")
        encrypted_message = XORCipher.encrypt(binary_message)
        print(f"Encrypted message: {encrypted_message}")
        signal = LineCode2B1Q.apply_2b1q(encrypted_message)
        print(f"Signal: {signal}")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(bytes([byte + 128 for byte in signal]))
            print("Mensagem enviada:", signal)