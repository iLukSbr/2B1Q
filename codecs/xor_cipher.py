class XORCipher:
    def __init__(self, key):
        self.key = key

    @staticmethod
    def encrypt(self, text):
        return ''.join(chr(ord(text[i]) ^ ord(self.key[i % len(self.key)])) for i in range(len(text)))

    @staticmethod
    def decrypt(self, text):
        return ''.join(chr(ord(text[i]) ^ ord(self.key[i % len(self.key)])) for i in range(len(text)))
