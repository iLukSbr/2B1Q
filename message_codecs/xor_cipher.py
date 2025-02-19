from message_codecs import KeyManager

"""
A cifra XOR usa uma chave para criptografar e descriptografar uma mensagem.
A operação resulta em 1 se os bits da mensagem e da chave são diferentes e 0 se forem iguais.
A chave é repetida ou aparada para que tenha o mesmo tamanho da mensagem.
Retirado da biblioteca de cifras do Python.
"""
class XORCipher:
    key = None

    """
    Inicializa a chave se não houver.
    """
    @staticmethod
    def initialize_key():
        if XORCipher.key is None:
            XORCipher.key = KeyManager.get_binary_key()
            if not XORCipher.key:
                raise ValueError("Failed to initialize the key.")

    """
    Criptografa uma mensagem usando a cifra XOR.
    """
    @staticmethod
    def encrypt(bit_array):
        XORCipher.initialize_key()
        encrypted_bits = []
        for i in range(len(bit_array)):
            encrypted_bits.append(bit_array[i] ^ XORCipher.key[i % len(XORCipher.key)])
        return encrypted_bits

    """
    Descriptografa uma mensagem usando a cifra XOR.
    """
    @staticmethod
    def decrypt(bit_array):
        XORCipher.initialize_key()
        decrypted_bits = []
        for i in range(len(bit_array)):
            decrypted_bits.append(bit_array[i] ^ XORCipher.key[i % len(XORCipher.key)])
        return decrypted_bits