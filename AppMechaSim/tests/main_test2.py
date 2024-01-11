import tkinter as tk

def on_resize(event):
    # Update the scroll region to encompass the bounding box of all elements on the canvas
    canvas.configure(scrollregion=canvas.bbox("all"))

root = tk.Tk()
root.geometry('500x500')  # Set the size of the window

# Create a frame and pack it to fill the entire window
frame_addable = tk.Frame(root, bg="blue")
frame_addable.pack(fill="both", expand=True)

# Create a canvas and a scrollbar
canvas = tk.Canvas(frame_addable)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(frame_addable, orient="vertical", command=canvas.yview)
scrollbar.pack(side="left", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the buttons
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Add many buttons to the frame
for i in range(50):
    button = tk.Button(frame, text="Button " + str(i))
    button.grid(row=i, column=0, padx=100)  # Position the buttons 100 pixels from the left edge of the frame

# Bind the <Configure> event to the on_resize function
root.bind('<Configure>', on_resize)

root.mainloop()