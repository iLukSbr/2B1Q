"""
The XOR cipher uses a key to encrypt and decrypt a message.
The operation results in 1 if the bits of the message and the key are different and 0 if they are the same.
The key is repeated so that it has the same size as the message.
"""

from message_codecs import KeyManager

class XORCipher:
    key = KeyManager.get_binary_key()

    @staticmethod
    def encrypt(bit_array):
        if XORCipher.key is None:
            raise ValueError("A chave não foi definida.")
        encrypted_bits = []
        for i in range(len(bit_array)):
            encrypted_bits.append(bit_array[i] ^ XORCipher.key[i % len(XORCipher.key)])
        return encrypted_bits

    @staticmethod
    def decrypt(bit_array):
        if XORCipher.key is None:
            raise ValueError("A chave não foi definida.")
        decrypted_bits = []
        for i in range(len(bit_array)):
            decrypted_bits.append(bit_array[i] ^ XORCipher.key[i % len(XORCipher.key)])
        return decrypted_bits
