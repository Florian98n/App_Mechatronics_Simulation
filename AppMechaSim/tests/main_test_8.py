import tkinter as tk

def zoom_in(event=None):
    canvas.scale("all", 0, 0, 1.1, 1.1)
    canvas.configure(scrollregion=canvas.bbox("all"))

def zoom_out(event=None):
    canvas.scale("all", 0, 0, 0.9, 0.9)
    canvas.configure(scrollregion=canvas.bbox("all"))

root = tk.Tk()

# Create a frame for the canvas and scrollbars
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Add horizontal scrollbar to the frame
hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
hbar.pack(side=tk.BOTTOM, fill=tk.X)

# Add vertical scrollbar to the frame
vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create the canvas and add it to the frame
canvas = tk.Canvas(frame, bg='white', xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Configure the scrollbars to move the canvas
hbar.config(command=canvas.xview)
vbar.config(command=canvas.yview)

# Add a few lines to the canvas
for i in range(10):
    canvas.create_line(i * 10, i * 10, i * 20, i * 20, tags="all")

# Add zoom in and zoom out buttons
zoom_in_button = tk.Button(root, text="Zoom in", command=zoom_in)
zoom_in_button.pack(side=tk.LEFT)
zoom_out_button = tk.Button(root, text="Zoom out", command=zoom_out)
zoom_out_button.pack(side=tk.LEFT)

canvas.configure(scrollregion=(-500, -500, 500, 500))

root.mainloop()