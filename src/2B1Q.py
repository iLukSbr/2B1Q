# Função para aplicar o algoritmo 2B1Q
def apply_2B1Q(data):
    # Estado inicial
    previous_level = "+1"
    # Mapeamento do algoritmo 2B1Q para cada par de bits
    previous_level_pos = {
        '00': '+1',
        '01': '+3',
        '10': '-1',
        '11': '-3'
    }
    previous_level_neg = {
        '00': '-1',
        '01': '-3',
        '10': '+1',
        '11': '+3'
    }

    signal = []

    # Percorre os bits de 2 em 2
    for i in range(0, len(data), 2):
        pair = data[i:i + 2]

        # Verifica se o par de bits está no mapeamento
        if "+" in previous_level:
            if pair in previous_level_pos:
                current_signal = previous_level_pos[pair]
            else:
                # Em caso de erro, mantém o último sinal para evitar transições abruptas
                current_signal = previous_level

        elif "-" in previous_level:
            if pair in previous_level_neg:
                current_signal = previous_level_neg[pair]
            else:
                # Em caso de erro, mantém o último sinal para evitar transições abruptas
                current_signal = previous_level

        else:
            # Em caso de erro, mantém o último sinal para evitar transições abruptas
            current_signal = previous_level

        # Adiciona o sinal atual à lista de sinais
        signal.append(current_signal)
        previous_level = current_signal

    return ''.join(signal)

# Função para aplicar o algoritmo de codificação de linha inverso
def decode_2B1Q(data):
    # Estado inicial
    previous_level = "+1"
    # Mapeamento do algoritmo 2B1Q inverso
    previous_level_pos_inverse = {
        '+1': '00',
        '+3': '01',
        '-1': '10',
        '-3': '11'
    }
    previous_level_neg_inverse = {
        '-1': '00',
        '-3': '01',
        '+1': '10',
        '+3': '11'
    }

    bits = []

    # Estado inicial
    state = '00'
    aaaas=0

    # Percorre os bits de 2 em 2
    for i in range(0, len(data), 2):
        pair = data[i:i + 2]

        # Verifica se o par de bits está no mapeamento
        if "+" in previous_level:
            if pair in previous_level_pos_inverse:
                current_bits = previous_level_pos_inverse[pair]
            else:
                # Em caso de erro, mantém o último sinal para evitar transições abruptas
                current_bits = state

        elif "-" in previous_level:
            if pair in previous_level_neg_inverse:
                current_bits = previous_level_neg_inverse[pair]
            else:
                # Em caso de erro, mantém o último sinal para evitar transições abruptas
                current_bits = state

        else:
            # Em caso de erro, mantém o último sinal para evitar transições abruptas
            current_bits = state

        # Adiciona o sinal atual à lista de sinais
        bits.append(current_bits)
        previous_level = pair

    return ''.join(bits)
