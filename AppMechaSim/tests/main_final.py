import tkinter as tk
from tkinter import ttk

global frame_simulation_buttons, root, frame_search_addable, frame_addable_list, frame_workspace


def on_resize(event):
    global frame_simulation_buttons, root, frame_search_addable, frame_addable_list, frame_workspace
    w_event = event.width
    h_event = event.height
    if w_event >= 350 and h_event >= 200:
        print('Window resized to x:', w_event, ' y:', h_event)
        if w_event > 450:
            frame_simulation_buttons.place(x=root.winfo_width() / 2 - frame_simulation_buttons.winfo_width() / 2, y=35)
            frame_workspace.configure(width=root.winfo_width() - 110 - 5)
        if h_event > 200:
            frame_addable_list.configure(height=root.winfo_height() - 90 - 5)
            frame_workspace.configure(height=root.winfo_height() - 35 - 5)


def main():
    global frame_simulation_buttons, root, frame_search_addable, frame_addable_list, frame_workspace
    root = tk.Tk()
    root.title("Path + name of file")
    root.minsize(400, 250)
    root.bind('<Configure>', on_resize)
    root.geometry("500x300")
    # root.state("zoomed")

    frame_file_control = tk.Frame(root, width=400, height=30, bg="red")
    frame_file_control.place(x=0, y=0)

    frame_search_addable = tk.Frame(root, width=100, height=50, bg="green")
    frame_search_addable.place(x=5, y=35)

    frame_addable_list = tk.Frame(root, width=100, height=50, bg="blue")
    frame_addable_list.place(x=5, y=90)

    frame_workspace = tk.Frame(root, width=100, height=50, bg="gray")
    frame_workspace.place(x=110, y=35)

    frame_simulation_buttons = tk.Frame(root, width=200, height=50, bg="yellow")
    frame_simulation_buttons.place(x=root.winfo_width() / 2 - frame_simulation_buttons.winfo_width() / 2, y=35)

    root.mainloop()


if __name__ == '__main__':
    main()

    # btn1 = tk.Button(frame, text="Button 1", command=create_buttons)
    # btn1.pack(side="top", fill="x")
