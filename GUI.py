import tkinter as tk
from tkinter import ttk
import subprocess

def update_variables():
    speed_value = int(speed_entry.get())
    smooth_value = int(smooth_entry.get())

    # Update the values in main.py using subprocess
    subprocess.run(["python", "main.py", "--update-variables", str(speed_value), str(smooth_value)])

# Create the main application window
root = tk.Tk()
root.title("Variable Updater")

# Create and pack labels and entry fields for speed and smooth variables
speed_label = ttk.Label(root, text="Speed:")
speed_label.pack()
speed_entry = ttk.Entry(root)
speed_entry.pack()

smooth_label = ttk.Label(root, text="Smooth:")
smooth_label.pack()
smooth_entry = ttk.Entry(root)
smooth_entry.pack()

# Create a button to update the variables
update_button = ttk.Button(root, text="Update Variables", command=update_variables)
update_button.pack()

# Start the GUI main loop
root.mainloop()
