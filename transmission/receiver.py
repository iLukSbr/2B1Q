import socket
import configparser
from cryptography import decrypt_message

class MessageReceiver:
    @staticmethod
    def receive_message():
        config = configparser.ConfigParser()
        config.read('config.ini')
        host = config['server']['host']
        port = int(config['server']['port'])

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print("Aguardando conexão...")
            conn, addr = s.accept()
            with conn:
                print(f"Conectado por {addr}")
                encrypted_message = conn.recv(1024).decode('utf-8')
                decoded_message = decrypt_message(encrypted_message)
                signal = [int(bit) for bit in encrypted_message]
                print(f"Mensagem recebida: {decoded_message}")
                return encrypted_message, decoded_message, signal