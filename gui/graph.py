import matplotlib.pyplot as plt

class Graph:
    @staticmethod
    def plot_voltage_time(data, title, filename):
        plt.figure(figsize=(10, 5))
        plt.plot(data, marker='o')
        plt.title(title)
        plt.xlabel('Time')
        plt.ylabel('Voltage')
        plt.grid(True)
        plt.savefig(filename)
        plt.close()