"""
A cifra XOR usa uma chave para criptografar e descriptografar uma mensagem.
A operação resulta 1 se os bits da mensagem e da chave forem diferentes e 0 se forem iguais.
A chave é repetida para que tenha o mesmo tamanho da mensagem.
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
