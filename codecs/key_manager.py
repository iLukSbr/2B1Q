from cryptography.fernet import Fernet

class KeyManager:
    def __init__(self):
        self.key_path = '.credentials'
        self.key = None
        self.load_key()

    def load_key(self):
        with open(self.key_path, 'rb') as f:
            self.key = f.read()

    def save_key(self):
        with open(self.key_path, 'wb') as f:
            f.write(self.key)

    def generate_key(self):
        self.key = Fernet.generate_key()
        self.save_key()

    def encrypt(self, data):
        f = Fernet(self.key)
        return f.encrypt(data)

    def decrypt(self, data):
        f = Fernet(self.key)
        return f.decrypt(data)