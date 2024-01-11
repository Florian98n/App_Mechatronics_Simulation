import tkinter as tk
from PIL import Image, ImageTk
#import Pneumatics_Objects_File
import Parameters_Window_File
import Photos_File


class WorkspaceSizeFrame:
    def __init__(self, root, update_rectangle_canvas):
        self.root = root
        self.update_rectangle_canvas = update_rectangle_canvas
        self.x = 0
        self.y = 0
        self.error_flag = 0
        self.new_width = 0
        self.new_height = 0
        self.width_var = tk.StringVar(value='10')
        self.height_var = tk.StringVar(value='5')
        self.draggable_window = tk.Frame(self.root, bg='black', bd=1, width=500, height=500)

        # first layer
        self.title_bar = tk.Frame(self.draggable_window, bg='white', height=20, width=50)
        self.title_bar.pack(side='top', fill='x')
        self.button_x = tk.Button(self.title_bar, text='X', width=5, command=self.close_change_workspace_size_frame)
        self.button_x.pack(side='right')
        self.background_default_color = self.button_x['bg']
        self.button_x.bind("<Enter>", self.on_enter)
        self.button_x.bind("<Leave>", self.on_leave)

        # second layer
        self.frame_change_size_text = tk.Frame(self.draggable_window, bg='lightblue', highlightbackground='black', highlightthickness=1, width=400, height=150)
        self.frame_change_size_text.pack(side='top', fill='x')

        self.text_width = tk.Label(self.frame_change_size_text, bg='lightblue', text="New width: ")
        self.text_width.place(x=20, y=10)
        self.text_width_numbers = tk.Label(self.frame_change_size_text, bg='lightblue', text="10<=                       <=100")
        self.text_width_numbers.place(x=158, y=20, anchor='center')
        self.entry_width = tk.Entry(self.frame_change_size_text,
                                    textvariable=self.width_var,
                                    width=10)
        self.entry_width.place(x=155, y=20, anchor='center')

        self.text_height = tk.Label(self.frame_change_size_text, bg='lightblue', text="New height:")
        self.text_height.place(x=20, y=50)
        self.text_width_numbers = tk.Label(self.frame_change_size_text, bg='lightblue', text="5<=                       <=50")
        self.text_width_numbers.place(x=158, y=60, anchor='center')
        self.entry_height = tk.Entry(self.frame_change_size_text,
                                     textvariable=self.height_var,
                                     width=10)
        self.entry_height.place(x=155, y=60, anchor='center')

        self.button_save = tk.Button(self.frame_change_size_text, width=8, text='Save', command=self.save_button_pushed)
        self.button_save.place(x=250, y=100)

        self.title_bar.bind('<ButtonPress-1>', self.start_drag)
        self.title_bar.bind('<ButtonRelease-1>', self.stop_drag)
        self.title_bar.bind('<B1-Motion>', self.do_drag)

        self.text_invalid = tk.Label(self.frame_change_size_text, fg='red', bg='lightblue', text="Invalid values")

    def save_button_pushed(self):
        try:
            self.error_flag = 0
            width = int(self.width_var.get())
            if 9 < width < 101:
                self.new_width = width
            else:
                self.error_flag = 1
            height = int(self.height_var.get())
            if 4 < height < 51:
                self.new_height = height
            else:
                self.error_flag = 1
        except ValueError:
            self.error_flag = 1
        if self.error_flag:
            self.text_invalid.place(x=150, y=100)
        else:
            self.text_invalid.place_forget()
            self.update_rectangle_canvas(self.new_width, self.new_height)
            self.draggable_window.place_forget()

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

    def open_workspace_change_size_frame(self):
        self.draggable_window.place(x=175, y=20)

    def close_change_workspace_size_frame(self):
        self.draggable_window.place_forget()

    def on_enter(self, event):
        self.button_x.configure(background='red')

    def on_leave(self, event):
        self.button_x.configure(background=self.background_default_color)
