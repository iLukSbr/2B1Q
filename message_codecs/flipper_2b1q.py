"""
Class for encoding and decoding 2B1Q signals with polarity inversion after each pair of bits usage.
"""

import copy

class Flipper2B1Q:
    voltage = {
        '00': 1,
        '01': 3,
        '10': -1,
        '11': -3
    }

    @staticmethod
    def binary_to_voltage(data):
        encoded = []
        voltage_tmp = copy.deepcopy(Flipper2B1Q.voltage)
        previous_2b = None
        for i in range(0, len(data), 2):
            pair = ''.join(map(str, data[i:i + 2]))  # Convert list of integers to string
            if previous_2b == pair:
                voltage_tmp[pair] *= -1
                for key, value in voltage_tmp.items():
                    if pair != key and value == voltage_tmp[pair]:
                        voltage_tmp[key] *= -1
                        break
            encoded.append(voltage_tmp[pair])
            previous_2b = pair
        return encoded

    @staticmethod
    def voltage_to_binary(data):
        decoded = []
        voltage_tmp = copy.deepcopy(Flipper2B1Q.voltage)
        previous_2b = None
        for value in data:  # For each voltage value
            for key, val in voltage_tmp.items():  # For each 2-bit pair
                if val == value:  # If the voltage value matches the 2-bit pair
                    if previous_2b == key:  # If the 2-bit pair is the same as the previous one
                        voltage_tmp[key] = -val  # Invert the voltage value
                        for k, v in voltage_tmp.items():  # Invert the other 2-bit pair
                            if k != key and v == -val:  # If the voltage value matches the inverted value
                                voltage_tmp[k] = -v  # Invert the voltage value
                                break
                    decoded.append(key)
                    previous_2b = key
                    break
        return [int(bit) for pair in decoded for bit in pair]