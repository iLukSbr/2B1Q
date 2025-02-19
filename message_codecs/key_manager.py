from cryptography.fernet import Fernet
from tests.logger import Logger
import os
import base64

"""
Fermat usa um gerador de números aleatórios criptograficamente seguro para gerar 32 bytes de dados aleatórios.
Isso é feito usando a função os.urandom ou uma função equivalente que fornece bytes aleatórios seguros.
Os 32 bytes de dados aleatórios são então codificados em base64 para produzir uma string de 44 caracteres.
A codificação Base64 é usada para garantir que a chave possa ser representada como uma string ASCII segura para armazenamento e transmissão.
Código retirado do repositório de criptografia do Python.
"""
class KeyManager:
    logger = Logger().get_logger()
    key = None

    """
    Obtém o caminho do arquivo crypto.key da chave.
    """
    @staticmethod
    def get_key_path():
        script_dir = os.path.dirname(__file__)
        return os.path.join(script_dir, 'crypto.key')

    """
    Carrega o arquivo da chave se existir, caso contrário, gera uma nova chave.
    """
    @staticmethod
    def load_key():
        key_path = KeyManager.get_key_path()
        if os.path.exists(key_path):
            with open(key_path, 'rb') as f:
                KeyManager.key = f.read()
                if not KeyManager.key:
                    KeyManager.logger.info(f"Key file {key_path} is empty, generating new key.")
                    KeyManager.generate_key()
                else:
                    KeyManager.logger.info(f"Key loaded from {key_path}")
        else:
            KeyManager.generate_key()

    """
    Salva a chave no arquivo crypto.key.
    """
    @staticmethod
    def save_key():
        key_path = KeyManager.get_key_path()
        with open(key_path, 'wb') as f:
            f.write(KeyManager.key)
        KeyManager.logger.info(f"Key saved to {key_path}")

    """
    Gera uma nova chave e a salva no arquivo crypto.key.
    """
    @staticmethod
    def generate_key():
        KeyManager.key = Fernet.generate_key()
        KeyManager.save_key()
        KeyManager.logger.info("New key generated")

    @staticmethod
    def get_raw_key():
        if KeyManager.key is None:
            KeyManager.load_key()
        if not KeyManager.key:
            raise ValueError("Failed to load or generate the key.")
        return KeyManager.key

    @staticmethod
    def get_decoded_key():
        raw_key = KeyManager.get_raw_key()
        return base64.urlsafe_b64decode(raw_key)

    @staticmethod
    def get_binary_key():
        decoded_key = KeyManager.get_decoded_key()
        return [int(bit) for byte in decoded_key for bit in bin(byte)[2:].zfill(8)]