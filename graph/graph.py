import matplotlib.pyplot as plt
import os
import webbrowser

from tests.logger import Logger

"""
Classe geradora de gráficos.
"""
class Graph:
    logger = Logger().get_logger()

    """
    Gera um gráfico do sinal 2B1Q.
    """
    @staticmethod
    def create_graph(data, title, filename):
        # Mapeia os valores de tensão para posições no gráfico
        y_positions = {-3: 0, -1: 2, 1: 4, 3: 6}
        y = [y_positions[value] for value in data]

        x = list(range(len(data)))

        plt.step(x, y, where='post')
        plt.yticks([0, 2, 4, 6], ['-3', '-1', '1', '3'])
        plt.title(title)
        plt.xlabel('Time')
        plt.ylabel('State')
        plt.savefig(filename, format='svg')
        Graph.logger.info(f"Graph saved as {filename}")
        plt.close()

        # Abre o arquivo .svg no navegador padrão
        webbrowser.open(f'file://{os.path.abspath(filename)}')
