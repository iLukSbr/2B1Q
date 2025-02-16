class ISDN2B1Q:
    def __init__(self):
        self.voltage = {
            '00': -3,
            '01': -1,
            '10': 3,
            '11': 1
        }
        self.code = {v: k for k, v in self.voltage.items()}

    @staticmethod
    def binary_to_voltage(self, data):
        encoded = []
        for i in range(0, len(data), 2):
            encoded.append(self.voltage[data[i:i+2]])
        return encoded

    @staticmethod
    def voltage_to_binary(self, data):
        decoded = []
        for value in data:
            decoded.append(self.code[value])
        return ''.join(decoded)
