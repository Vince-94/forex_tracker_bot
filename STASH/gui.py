import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib.figure import Figure

class MyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Matplotlib GUI")

        # Matplotlib section
        self.fig, self.ax = plt.subplots(figsize=(5, 3), tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.draw()

        # Time section
        self.time_label = ttk.Label(root, text="Current Time:")
        self.time_label.pack()

        # Value section
        self.value_label = ttk.Label(root, text="Current Value:")
        self.value_label.pack()

        # Update button
        update_button = ttk.Button(root, text="Update", command=self.update_values)
        update_button.pack()

    def update_values(self):
        # Update time
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"Current Time: {current_time}")

        # Update value (replace this with your data retrieval logic)
        current_value = 42  # Replace with actual value
        self.value_label.config(text=f"Current Value: {current_value}")

        # Update graph (replace this with your data plotting logic)
        # For demonstration purposes, plotting a random point on the graph
        self.ax.cla()
        self.ax.plot(datetime.now(), current_value, 'ro')  # 'ro' means red color, circle marker
        self.ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.set_title('Real-time Data')
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    my_gui = MyGUI(root)
    root.mainloop()
