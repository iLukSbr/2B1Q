import os
import socket
import time

from graph import Graph
from message_codecs import *
from tests import Logger

"""
Classe que envia mensagens para o servidor.
"""
class MessageSender:
    logger = Logger().get_logger()
    state_duration = 1 # microseconds
    test_slides = False

    """
    Transforma a mensagem em binário, depois em 
    """
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

        script_dir = os.path.dirname(__file__)
        relative_path = os.path.join(script_dir, '../gui/sent_signal.svg')
        Graph.create_graph(signal, "Sent 2B1Q signal", relative_path)

        # Retorna os detalhes da mensagem em um dicionário.
        return {
            "status": "Ready to Send",
            "raw_message": message,
            "binary_message": binary_message,
            "encrypted_message": encrypted_message,
            "encoded_message": signal
        }

    """
    Envia um sinal para o servidor.
    """
    @staticmethod
    def send_signal(signal, host, port):
        port = int(port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            for value in signal:
                s.sendall(bytes([int(value) + 128]))
                MessageSender.logger.info(f"Sent value: {value}")
                time.sleep(MessageSender.state_duration / 1000000)
