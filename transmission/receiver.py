import socket
import configparser
from message_codecs import *

class MessageReceiver:
    state_duration = 500 # milliseconds

    @staticmethod
    def receive_message(self):
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
                self.signal = list(data)
                self.encrypted_message = Flipper2B1Q.voltage_to_binary(signal)
                self.decoded_message = XORCipher.decrypt(encrypted_message)
                self.message = BinaryConverter.utf8_from_binary(decoded_message)
                print(f"Mensagem recebida: {self.message}")
                return self.message
