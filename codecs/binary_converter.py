class BinaryConverter:
    def __init__(self):
        return

    @staticmethod
    def utf8_to_binary(data):
        return ''.join(format(ord(char), '08b') for char in data)

    @staticmethod
    def utf8_from_binary(data):
        return ''.join(chr(int(data[i: i +8], 2)) for i in range(0, len(data), 8))
