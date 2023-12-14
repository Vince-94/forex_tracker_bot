import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time



def generate_data():
    current_time = time.time()
    values = np.sin(current_time)
    return current_time, values


def update(frame):
    current_time, values = generate_data()
    x_data.append(current_time)
    y_data.append(values)

    # Keep only the last N points
    N = 10

    line.set_data(x_data[-N:], y_data[-N:])


    # Set axis limits to ensure the new data is visible
    ax.relim()
    ax.autoscale_view()

    return line,


def init():
    line.set_data([], [])
    # ax.set_xlim(0, 10)  # Set initial x-axis limits
    # ax.set_ylim(-1, 1)  # Set initial y-axis limits
    return line,


def plot():
    global x_data, y_data, line, ax

    x_data, y_data = [], []

    fig, ax = plt.subplots()
    line, = ax.plot([], [], 'bo-', label='Values')
    ax.set_xlabel('Current Time')
    ax.set_ylabel('Values')
    ax.legend()

    ani = FuncAnimation(fig, update, frames=range(0, 10), init_func=init, blit=True, interval=1000)
    plt.show()



def main():
    plot()

if __name__ == "__main__":
    main()
