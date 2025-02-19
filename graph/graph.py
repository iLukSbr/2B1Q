import matplotlib.pyplot as plt
from tests.logger import Logger

class Graph:
    logger = Logger().get_logger()

    @staticmethod
    def create_graph(data, title, filename):
        # Map signal values to y-axis positions
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