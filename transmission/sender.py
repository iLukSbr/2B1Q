import socket
import configparser
import time
from message_codecs import *

class MessageSender:
    @staticmethod
    def send_message(self, message):
        config = configparser.ConfigParser()
        config.read('config.ini')
        host = config['server']['host']
        port = int(config['server']['port'])
        bit_interval = int(config['server']['bit_interval'])
        stop_interval = int(config['server']['stop_interval'])

        # Add STX and ETX to the message
        self.message = f'\x02{message}\x03'
        self.binary_message = BinaryConverter.utf8_to_binary(message)
        self.encrypted_message = XORCipher.encrypt(self.binary_message)
        self.message_signal = Flipper2B1Q.binary_to_voltage(self.encrypted_message)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            for bit in self.message_signal:
                s.sendall(bit.encode('utf-8'))
                time.sleep(bit_interval)
            time.sleep(stop_interval)
            print(f"Mensagem enviada: {self.message_signal}")