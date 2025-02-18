import matplotlib.pyplot as plt

# Função para criar o gráfico
def create_graph(data, titulo):
    tuple_data = tuple(data[i:i+2] for i in range(0, len(data), 2))  # Agrupa os dados em pares
    x = list(range(len(tuple_data)))

    # Configura posições dos elementos no eixo y
    y_positions = {"-3": 0, "-1": 2, "+1": 4, "+3": 6}
    y = [y_positions[str(value)] for value in tuple_data]

    plt.step(x, y, where='post')
    plt.yticks([0, 2, 4, 6], ['-3', '-1', '+1', '+3'])
    plt.title(titulo)
    plt.xlabel('Tempo')
    plt.ylabel('Estado')
    plt.show(block=False)