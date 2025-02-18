import socket
import configparser
import os
from message_codecs import *

class MessageReceiver:
    state_duration = 500  # milliseconds

    @staticmethod
    def receive_message():
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
            s.bind((host, port))
            s.listen()
            print("Aguardando conexão...")
            conn, addr = s.accept()
            with conn:
                print(f"Conectado por {addr}")
                data = b''
                muted_count = 0
                while True:
                    chunk = conn.recv(1024)
                    if not chunk:
                        muted_count += 1
                        if muted_count >= 3:
                            print("End of message")
                            break
                    else:
                        muted_count = 0
                        data += chunk
                print(f"Raw data received: {data}")
                signal = [byte - 128 for byte in data]  # Map byte values back to voltage values
                print(f"Signal: {signal}")
                encrypted_message = LineCode2B1Q.decode_2b1q(signal)
                print(f"Encrypted message: {encrypted_message}")
                encrypted_message = [int(bit) for bit in encrypted_message]  # Convert string to list of integers
                decoded_message = XORCipher.decrypt(encrypted_message)
                print(f"Decoded message: {decoded_message}")
                message = BinaryConverter.utf8_from_binary(decoded_message)
                print(f"Mensagem recebida: {message}")
                return message