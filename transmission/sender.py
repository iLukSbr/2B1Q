import socket
import configparser
import os
import time
from message_codecs import *
from tests import Logger
from graph import Graph

class MessageSender:
    logger = Logger().get_logger()
    state_duration = 1 # microseconds
    test_slides = True

    @staticmethod
    def prepare_message(message):
        if not MessageSender.test_slides:
            MessageSender.logger.info(f"Message to send: {message}")
            binary_message = BinaryConverter.utf8_to_binary(message)
            MessageSender.logger.info(f"Binary message: {binary_message}")
            encrypted_message = XORCipher.encrypt(binary_message)
            MessageSender.logger.info(f"Encrypted message: {encrypted_message}")
            signal = LineCode2B1Q.apply_2b1q(encrypted_message)
            MessageSender.logger.info(f"Signal: {signal}")

        else:
            binary_message = None
            encrypted_message = None
            signal = [1,-3,-3,1,3]
            MessageSender.logger.info(f"Signal: {signal}")

        Graph.create_graph(signal, "Sent 2B1Q signal", "gui/sent_signal.svg")

        # Return the details as a JSON object
        return {
            "status": "Ready to Send",
            "raw_message": message,
            "binary_message": binary_message,
            "encrypted_message": encrypted_message,
            "encoded_message": signal
        }

    @staticmethod
    def send_signal(signal, host, port):
        port = int(port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            for value in signal:
                s.sendall(bytes([int(value) + 128]))
                MessageSender.logger.info(f"Sent value: {value}")
                time.sleep(MessageSender.state_duration / 1000000)