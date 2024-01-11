from tkinter import Tk, Button, PhotoImage

# Create a Tkinter window
root = Tk()

# Load an image
photo = PhotoImage(file="start_button.png")

# Define the function to be executed when the button is pressed
def start_button_pushed():
    print("Button pressed!")

# Create a button with the image and the function
button_start = Button(root, image=photo, command=start_button_pushed)

# Display the button
button_start.pack()

# Start the Tkinter event loop
root.mainloop()