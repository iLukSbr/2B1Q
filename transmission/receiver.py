from message_codecs import *
from tests import Logger
from graph import Graph
import tkinter as tk
from tkinter import messagebox

"""
Esta classe utiliza as funções de decodificação e descriptografia  do message_codecs para receber mensagens.
"""
class MessageReceiver:
    logger = Logger().get_logger()
    message = None
    decoded_message = None
    encrypted_message = None
    signal = None
    test_slides = False

    """
    Esta função recebe uma conexão e lê os dados recebidos em 3 tentativas.
    """
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

        MessageReceiver.signal = [byte - 128 for byte in data]

        if not MessageReceiver.test_slides:
              # Map byte values back to voltage values
            MessageReceiver.logger.info(f"Received data: {MessageReceiver.signal}")
            encrypted_message = LineCode2B1Q.decode_2b1q(MessageReceiver.signal)
            MessageReceiver.encrypted_message = [int(bit) for bit in encrypted_message]  # Convert string to list of integers
            MessageReceiver.logger.info(f"Encrypted message: {MessageReceiver.encrypted_message}")
            MessageReceiver.decoded_message = XORCipher.decrypt(MessageReceiver.encrypted_message)
            MessageReceiver.logger.info(f"Decoded message: {MessageReceiver.decoded_message}")
            MessageReceiver.message = BinaryConverter.utf8_from_binary(MessageReceiver.decoded_message)
            MessageReceiver.logger.info(f"Message: {MessageReceiver.message}")

        else:
            MessageReceiver.logger.info(f"Received data: {MessageReceiver.signal}")
            MessageReceiver.encrypted_message = LineCode2B1Q.decode_2b1q(MessageReceiver.signal)
            MessageReceiver.logger.info(f"Encrypted message: {MessageReceiver.encrypted_message}")
            MessageReceiver.decoded_message = MessageReceiver.encrypted_message
            MessageReceiver.message = BinaryConverter.utf8_from_binary(MessageReceiver.decoded_message)
            MessageReceiver.logger.info(f"Message: {MessageReceiver.message}")

        Graph.create_graph(MessageReceiver.signal, "Received 2B1Q Signal", "gui/received_signal.svg")

        # Return the details as a JSON object
        return {
            "message": MessageReceiver.message,
            "raw_message": MessageReceiver.decoded_message,
            "binary_message": MessageReceiver.encrypted_message,
            "encrypted_message": MessageReceiver.signal,
            "encoded_message": MessageReceiver.message
        }

    """
    Obtém a mensagem recebida por último do buffer.
    """
    @staticmethod
    def get_message_received():
        return {
            "message": MessageReceiver.message,
            "raw_message": MessageReceiver.decoded_message,
            "binary_message": MessageReceiver.encrypted_message,
            "encrypted_message": MessageReceiver.signal,
            "encoded_message": MessageReceiver.message
        }

    """
    Mostra uma janela de aviso com a mensagem recebida.
    """
    @staticmethod
    def show_message_received():
        message = MessageReceiver.get_message_received()
        message_text = (
            f"Message: {message['message']}\n"
            f"Raw Message: {message['raw_message']}\n"
            f"Binary Message: {message['binary_message']}\n"
            f"Encrypted Message: {message['encrypted_message']}\n"
            f"Encoded Message: {message['encoded_message']}"
        )
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showinfo("Message Received", message_text)
        root.destroy()