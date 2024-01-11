import tkinter as tk

class DraggableWindow:
    def __init__(self, root):
        self.root = root
        self.draggable_window = tk.Frame(self.root, bg='grey', bd=1, width=200, height=200)
        self.draggable_window.place(x=20, y=20)

        self.title_bar = tk.Frame(self.draggable_window, bg='white', height=20)
        self.title_bar.pack(side='top', fill='x')

        self.button_x = tk.Button(self.title_bar, text='X', width=5)
        self.button_x.pack(side='right')

        self.bottom_text = tk.Label(self.draggable_window, text="Frame with simulation buttons", bg='blue')
        self.bottom_text.pack(side='bottom')

        self.title_bar.bind('<ButtonPress-1>', self.start_drag)
        self.title_bar.bind('<ButtonRelease-1>', self.stop_drag)
        self.title_bar.bind('<B1-Motion>', self.do_drag)

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def stop_drag(self, event):
        self.x = None
        self.y = None

    def do_drag(self, event):
        dx = event.x_root - self.x - self.draggable_window.winfo_rootx()
        dy = event.y_root - self.y - self.draggable_window.winfo_rooty()
        x = self.draggable_window.winfo_x() + dx
        y = self.draggable_window.winfo_y() + dy
        self.draggable_window.place(x=x, y=y)

root = tk.Tk()
root.geometry("300x300")

button = tk.Button(root, text="Create Draggable Mini Window", command=lambda: DraggableWindow(root))
button.pack()

root.mainloop()