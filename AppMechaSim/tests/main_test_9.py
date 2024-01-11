import tkinter as tk
from PIL import ImageTk, Image

def show_menu(event):
    if canvas.find_withtag("current"):
        menu.post(event.x_root, event.y_root)

root = tk.Tk()

# Load your image
image = ImageTk.PhotoImage(Image.open('test_size1.png'))

# Create a canvas and add the image to it
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()
canvas.create_image(20, 20, anchor='nw', image=image)

# Create a menu
menu = tk.Menu(root, tearoff=0)
menu.add_command(label='Image')

# Bind right click event to the canvas
canvas.bind('<Button-3>', show_menu)

root.mainloop()