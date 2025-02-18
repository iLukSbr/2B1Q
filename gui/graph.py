import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio
import numpy as np
import time

class Graph:
    def __init__(self):
        self.fig = make_subplots(rows=1, cols=1)
        self.fig.update_layout(title='Real-Time Voltage Level', xaxis_title='Time', yaxis_title='Voltage',
                               showlegend=False)

        # Initial data and trace with glowing effect
        self.data = [0]
        self.x_data = [0]
        self.line_trace = go.Scatter(
            x=self.x_data,
            y=self.data,
            mode='lines',
            line=dict(color='blue', width=2)
        )
        self.head_trace = go.Scatter(
            x=[self.x_data[-1]],
            y=[self.data[-1]],
            mode='markers',
            marker=dict(size=10, color='red', opacity=0.8, symbol='circle')
        )

        self.fig.add_trace(self.line_trace)
        self.fig.add_trace(self.head_trace)

    def update_animation(self, frame):
        x, y = frame
        self.x_data.append(x)
        self.data.append(y)

        # Update trace data
        self.line_trace.x = self.x_data
        self.line_trace.y = self.data
        self.head_trace.x = [x]
        self.head_trace.y = [y]

        # Clear previous traces
        self.fig.data = []

        # Add updated traces
        self.fig.add_trace(self.line_trace)
        self.fig.add_trace(self.head_trace)

        # Adjust x-axis range for real-time view
        self.fig.update_xaxes(range=[max(0, x - 10), x + 1])

    def animate(self, data_stream):
        for frame in data_stream:
            self.update_animation(frame)
            time.sleep(0.1)  # Adjust the sleep time as needed

    def show(self):
        pio.show(self.fig, auto_open=True)