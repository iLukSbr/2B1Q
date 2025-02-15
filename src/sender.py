#!/usr/bin/env python

import socket
from cryptography import encrypt_message

def send_message(message):
    encrypted_message = encrypt_message(message)
    host = 'localhost'  # Endereço do servidor
    port = 12345        # Porta do servidor

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(encrypted_message.encode('utf-8'))
        print(f"Mensagem enviada: {encrypted_message}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python sender.py <mensagem>")
        sys.exit(1)
    message = sys.argv[1]
    send_message(message)