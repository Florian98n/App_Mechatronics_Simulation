import tkinter as tk

def on_button_click():
    button.config(relief=tk.SUNKEN, bd=3)

root = tk.Tk()

button = tk.Button(root, text="Click me", command=on_button_click)
button.pack()

root.mainloop()