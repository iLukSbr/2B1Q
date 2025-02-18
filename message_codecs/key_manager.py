"""
Fermat uses a cryptographically secure random number generator to generate 32 bytes of random data.
This is done using the os.urandom function or an equivalent function that provides secure random bytes.
The 32 bytes of random data are then encoded in base64 to produce a 44-character string.
Base64 encoding is used to ensure that the key can be represented as a secure ASCII string for storage and transmission.
"""

# message_codecs/key_manager.py
from cryptography.fernet import Fernet
from tests.logger import Logger
import os
import base64

class KeyManager:
    logger = Logger().get_logger()
    key = None

    @staticmethod
    def get_key_path():
        script_dir = os.path.dirname(__file__)
        return os.path.join(script_dir, 'crypto.key')

    @staticmethod
    def load_key():
        key_path = KeyManager.get_key_path()
        if os.path.exists(key_path):
            with open(key_path, 'rb') as f:
                KeyManager.key = f.read()
                if not KeyManager.key:
                    KeyManager.logger.debug(f"Key file {key_path} is empty, generating new key.")
                    KeyManager.generate_key()
                else:
                    KeyManager.logger.debug(f"Key loaded from {key_path}")
        else:
            KeyManager.generate_key()

    @staticmethod
    def save_key():
        key_path = KeyManager.get_key_path()
        with open(key_path, 'wb') as f:
            f.write(KeyManager.key)
        KeyManager.logger.debug(f"Key saved to {key_path}")

    @staticmethod
    def generate_key():
        KeyManager.key = Fernet.generate_key()
        KeyManager.save_key()
        KeyManager.logger.debug("New key generated")

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