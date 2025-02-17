"""
Utility to convert UTF-8 text to binary and vice versa.
"""

class BinaryConverter:
    @staticmethod
    def utf8_to_binary(string):
        return [int(bit) for char in string for bit in format(ord(char), '08b')]

    @staticmethod
    def utf8_from_binary(bit_array):
        chars = [chr(int(''.join(map(str, bit_array[i:i+8])), 2)) for i in range(0, len(bit_array), 8)]
        return ''.join(chars)