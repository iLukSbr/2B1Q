"""
Utilitário para converter mensagens de e para binário.
"""
class BinaryConverter:
    """
    Converte uma string para uma lista de bits.
    """
    @staticmethod
    def utf8_to_binary(string):
        return [int(bit) for char in string for bit in format(ord(char), '08b')]

    """
    Converte uma lista de bits para uma string.
    """
    @staticmethod
    def utf8_from_binary(bit_array):
        chars = [chr(int(''.join(map(str, bit_array[i:i+8])), 2)) for i in range(0, len(bit_array), 8)]
        return ''.join(chars)
