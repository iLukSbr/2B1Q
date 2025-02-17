import socket
import configparser
from cryptography import encrypt_message
from message_codecs import *

class MessageSender:
    @staticmethod
    def send_message(message):
        config = configparser.ConfigParser()
        config.read('config.ini')
        host = config['server']['host']
        port = int(config['server']['port'])

        binary_message = BinaryConverter.utf8_to_binary(message)
        encrypted_message = XORCipher.encrypt_message(binary_message)
        message_signal = ISDN2B1Q.binary_to_voltage(encrypted_message)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(encrypted_message.encode('utf-8'))
            print(f"Mensagem enviada: {encrypted_message}")