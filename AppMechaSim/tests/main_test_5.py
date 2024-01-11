import tkinter as tk

def create_menu(root):
    # Create a menubar
    menubar = tk.Menu(root)

    # Create a menu button labeled "File"
    filemenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=filemenu)

    # Add commands to the "File" button
    filemenu.add_command(label="New", command=lambda: print("New file"))
    filemenu.add_command(label="Open", command=lambda: print("Open file"))
    filemenu.add_command(label="Save", command=lambda: print("Save file"))

    # Display the menubar
    root.config(menu=menubar)

root = tk.Tk()
create_menu(root)
root.mainloop()