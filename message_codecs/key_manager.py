"""
Fernet usa um gerador de números aleatórios criptograficamente seguro para gerar 32 bytes de dados aleatórios.
Isso é feito usando a função os.urandom ou uma função equivalente que fornece bytes aleatórios seguros.
Os 32 bytes de dados aleatórios são então codificados em base64 para produzir uma string de 44 caracteres.
A codificação base64 é usada para garantir que a chave possa ser representada como uma string ASCII segura para armazenamento e transmissão.
"""

from cryptography.fernet import Fernet
import os
import base64

class KeyManager:
    key_path = '.credentials'
    key = None

    @staticmethod
    def load_key():
        if os.path.exists(KeyManager.key_path):
            with open(KeyManager.key_path, 'rb') as f:
                KeyManager.key = f.read()
        else:
            KeyManager.generate_key()

    @staticmethod
    def save_key():
        with open(KeyManager.key_path, 'wb') as f:
            f.write(KeyManager.key)

    @staticmethod
    def generate_key():
        KeyManager.key = Fernet.generate_key()
        KeyManager.save_key()

    @staticmethod
    def get_raw_key():
        if KeyManager.key is None:
            KeyManager.load_key()
        return KeyManager.key
    
    @staticmethod
    def get_decoded_key():
        raw_key = KeyManager.get_raw_key()
        return base64.urlsafe_b64decode(raw_key)

    @staticmethod
    def get_binary_key():
        decoded_key = KeyManager.get_decoded_key()
        return [int(bit) for byte in decoded_key for bit in bin(byte)[2:].zfill(8)]
