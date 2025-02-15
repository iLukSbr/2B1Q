#!/usr/bin/env python

import socket
from cryptography import decrypt_message

def receive_message():
    # Configuração do socket para receber a mensagem
    host = 'localhost'  # Endereço do servidor
    port = 12345        # Porta do servidor

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Aguardando conexão...")
        conn, addr = s.accept()
        with conn:
            print(f"Conectado por {addr}")
            encrypted_message = conn.recv(1024).decode('utf-8')
            decoded_message = decrypt_message(encrypted_message)
            signal = [int(bit) for bit in encrypted_message]  # Exemplo de sinal digital
            print(f"Mensagem recebida: {decoded_message}")
            return encrypted_message, decoded_message, signal

if __name__ == "__main__":
    receive_message()