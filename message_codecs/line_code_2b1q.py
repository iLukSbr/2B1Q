"""
    Algoritmo de codificação de linha 2B1Q.
"""

class LineCode2B1Q:
    # Função auxiliar para mapear pares de bits para sinais e vice-versa
    @staticmethod
    def map_bits_to_signal(pair, previous_level, mapping_pos, mapping_neg):
        if previous_level > 0:
            return mapping_pos.get(pair, previous_level)
        else:
            return mapping_neg.get(pair, previous_level)

    # Função para aplicar o algoritmo 2B1Q
    @staticmethod
    def apply_2b1q(data):
        # Estado inicial
        previous_level = 1
        # Mapeamento do algoritmo 2B1Q para cada par de bits
        previous_level_pos = {
            '00': 1,
            '01': 3,
            '10': -1,
            '11': -3
        }
        previous_level_neg = {
            '00': -1,
            '01': -3,
            '10': 1,
            '11': 3
        }

        signal = []

        # Percorre os bits de 2 em 2
        for i in range(0, len(data), 2):
            pair = ''.join(map(str, data[i:i + 2]))
            current_signal = LineCode2B1Q.map_bits_to_signal(pair, previous_level, previous_level_pos, previous_level_neg)
            # Adiciona o sinal atual à lista de sinais
            signal.append(current_signal)
            previous_level = current_signal

        return signal

    # Função para decodificar o sinal codificado em 2B1Q
    @staticmethod
    def decode_2b1q(data):
        # Estado inicial
        previous_level = 1
        # Mapeamento do algoritmo 2B1Q inverso
        previous_level_pos_inverse = {
            1: '00',
            3: '01',
            -1: '10',
            -3: '11'
        }
        previous_level_neg_inverse = {
            -1: '00',
            -3: '01',
            1: '10',
            3: '11'
        }

        bits = []

        # Percorre os valores do sinal
        for value in data:
            current_bits = LineCode2B1Q.map_bits_to_signal(value, previous_level, previous_level_pos_inverse, previous_level_neg_inverse)
            # Adiciona os bits atuais à lista de bits
            bits.append(current_bits)
            previous_level = value

        return ''.join(bits)