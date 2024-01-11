import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()

# Open the first image
image1 = Image.open("valve_3_2.png")

# Open the second image
image2 = Image.open("spring_for_valves.png")

# Combine the two images
combined_image = Image.new("RGBA", (image1.width + image2.width, max(image1.height, image2.height)), (0, 0, 0, 0))
combined_image.paste(image1, (0, 0))
combined_image.paste(image2, (image1.width, image2.height))

# Create a Tkinter PhotoImage object from the combined image
photo_image = ImageTk.PhotoImage(combined_image)

# Create a Tkinter canvas and display the image in it
canvas = tk.Canvas(root, width=combined_image.width, height=combined_image.height)
canvas.create_image(0, 0, anchor="nw", image=photo_image)
canvas.pack()

root.mainloop()