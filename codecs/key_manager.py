from cryptography.fernet import Fernet
import os

class KeyManager:
    def __init__(self):
        self.key_path = '.credentials'
        self.key = None
        self.load_key()

    def load_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, 'rb') as f:
                self.key = f.read()
        else:
            self.generate_key()

    def save_key(self):
        with open(self.key_path, 'wb') as f:
            f.write(self.key)

    def generate_key(self):
        self.key = Fernet.generate_key()
        self.save_key()

    def get_key(self):
        return self.key