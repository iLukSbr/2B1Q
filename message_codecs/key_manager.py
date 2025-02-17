"""
Fermat uses a cryptographically secure random number generator to generate 32 bytes of random data.
This is done using the os.urandom function or an equivalent function that provides secure random bytes.
The 32 bytes of random data are then encoded in base64 to produce a 44-character string.
Base64 encoding is used to ensure that the key can be represented as a secure ASCII string for storage and transmission.
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
