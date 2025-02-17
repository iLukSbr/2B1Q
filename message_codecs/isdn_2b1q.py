class ISDN2B1Q:
    voltage = {
        '00': 1,
        '01': 3,
        '10': -1,
        '11': -3
    }
    # code = 

    @staticmethod
    def binary_to_voltage(data):
        encoded = []
        last_2b = None
        # voltage_flipper = ISDN2B1Q.voltage
        # for i in range(0, len(data), 2):
        #     if last_2b is not None and last_2b == data[i:i+2]:
        #         encoded.append(-voltage_flipper[data[i:i+2]])
        #     else:
        #         encoded.append(voltage_flipper[data[i:i+2]])
                
            
        return encoded

    @staticmethod
    def voltage_to_binary(data):
        decoded = []
        # code_flipper = ISDN2B1Q.code
        # for value in data:
        #     decoded.append(code_flipper[value])
        #     code_flipper[value] = -code_flipper[code_flipper[value]]
        # return ''.join(decoded)