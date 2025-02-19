import socket
import configparser
import os
from message_codecs import *
from tests import Logger
from graph import Graph

class MessageReceiver:
    logger = Logger().get_logger()
    message = None
    decoded_message = None
    encrypted_message = None
    signal = None

    @staticmethod
    def receive_message(conn):
        data = b''
        muted_count = 0
        try:
            while True:
                chunk = conn.recv(1024)
                if not chunk:
                    muted_count += 1
                    if muted_count >= 3:
                        break
                else:
                    muted_count = 0
                    data += chunk
        except ConnectionResetError:
            MessageReceiver.logger.error("Connection was reset by the remote host")

        MessageReceiver.signal = [byte - 128 for byte in data]  # Map byte values back to voltage values
        MessageReceiver.logger.info(f"Received data: {MessageReceiver.signal}")
        Graph.create_graph(MessageReceiver.signal, "Received 2B1Q Signal", "../gui/received_signal.svg")
        encrypted_message = LineCode2B1Q.decode_2b1q(MessageReceiver.signal)
        MessageReceiver.encrypted_message = [int(bit) for bit in encrypted_message]  # Convert string to list of integers
        MessageReceiver.logger.info(f"Encrypted message: {MessageReceiver.encrypted_message}")
        MessageReceiver.decoded_message = XORCipher.decrypt(MessageReceiver.encrypted_message)
        MessageReceiver.logger.info(f"Decoded message: {MessageReceiver.decoded_message}")
        MessageReceiver.message = BinaryConverter.utf8_from_binary(MessageReceiver.decoded_message)
        MessageReceiver.logger.info(f"Message: {MessageReceiver.message}")

        # Return the details as a JSON object
        return {
            "message": MessageReceiver.message,
            "raw_message": MessageReceiver.decoded_message,
            "binary_message": MessageReceiver.encrypted_message,
            "encrypted_message": MessageReceiver.signal,
            "encoded_message": MessageReceiver.message
        }

    @staticmethod
    def get_message_received():
        return {
            "message": MessageReceiver.message,
            "raw_message": MessageReceiver.decoded_message,
            "binary_message": MessageReceiver.encrypted_message,
            "encrypted_message": MessageReceiver.signal,
            "encoded_message": MessageReceiver.message
        }