#!/usr/bin/env python

from cryptography.fernet import Fernet

# Geração de chave (isso deve ser feito uma vez e a chave deve ser armazenada de forma segura)
# key = Fernet.generate_key()
# with open("secret.key", "wb") as key_file:
#     key_file.write(key)

# Carregar a chave
def load_key():
    return open("secret.key", "rb").read()

key = load_key()
cipher_suite = Fernet(key)

def encrypt_message(message):
    # Criptografia da mensagem usando Fernet
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message.decode()

def decrypt_message(encrypted_message):
    # Descriptografia da mensagem usando Fernet
    decrypted_message = cipher_suite.decrypt(encrypted_message.encode())
    return decrypted_message.decode()