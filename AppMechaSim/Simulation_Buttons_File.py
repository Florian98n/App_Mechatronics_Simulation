import tkinter as tk
from PIL import Image, ImageTk
import Photos_File


class SimulationButtons:
    def __init__(self, root, update_sim_buttons_state):
        self.root = root
        self.update_sim_buttons_state = update_sim_buttons_state
        self.x = 0
        self.y = 0
        self.draggable_window = tk.Frame(self.root, bg='black', bd=1)

        # first layer
        self.title_bar = tk.Frame(self.draggable_window, bg='white', height=20, width=50)
        self.title_bar.pack(side='top', fill='x')
        self.button_x = tk.Button(self.title_bar, text='X', width=5, command=self.close_sim_buttons_frame)
        self.button_x.pack(side='right')
        self.background_default_color = self.button_x['bg']
        self.button_x.bind("<Enter>", self.on_enter)
        self.button_x.bind("<Leave>", self.on_leave)

        # second layer
        self.frame_sim_buttons = tk.Frame(self.draggable_window, bg='white',
                                          highlightbackground='black', highlightthickness=1, width=30, height=70)
        self.frame_sim_buttons.pack(side='top', fill='x')

        self.sim_start_flag = 0
        self.sim_continue_flag = 1
        self.photo_list = [ImageTk.PhotoImage]*4
        self.photo_list[0] = ImageTk.PhotoImage(Photos_File.simulation_buttons[0])
        self.photo_list[1] = ImageTk.PhotoImage(Photos_File.simulation_buttons[1])
        self.photo_list[2] = ImageTk.PhotoImage(Photos_File.simulation_buttons[2])
        self.photo_list[3] = ImageTk.PhotoImage(Photos_File.simulation_buttons[3])
        self.button_start = tk.Button(self.frame_sim_buttons, image=self.photo_list[0], command=self.start_button_pushed)
        self.button_start.pack(side='left', padx=5, pady=5)
        self.button_pause = tk.Button(self.frame_sim_buttons, image=self.photo_list[1], command=self.pause_continue_button_pushed)
        self.button_pause.pack(side='left', padx=5, pady=5)
        self.button_stop = tk.Button(self.frame_sim_buttons, image=self.photo_list[3], command=self.stop_button_pushed)
        self.button_stop.pack(side='left', padx=5, pady=5)

        # second layer
        self.frame_text = tk.Frame(self.draggable_window, bg='white', width=30, height=70)
        self.frame_text.pack(side='top', fill='x')

        self.text_state = tk.Label(self.frame_text, bg='white', text="Current state: Idle")
        self.text_state.pack(side='left')

        self.title_bar.bind('<ButtonPress-1>', self.start_drag)
        self.title_bar.bind('<ButtonRelease-1>', self.stop_drag)
        self.title_bar.bind('<B1-Motion>', self.do_drag)

        self.draggable_window.place(x=175, y=20)
    
    def start_button_pushed(self):
        if self.sim_start_flag == 0:
            self.sim_start_flag = 1
            self.button_start.config(relief=tk.SUNKEN, bd=3)
            self.text_state.config(text='Current state: Running')
            self.update_sim_buttons_state(self.sim_start_flag, self.sim_continue_flag)
        
    def stop_button_pushed(self):
        self.sim_start_flag = 0
        self.button_start.config(relief=tk.RAISED, bd=3)
        self.text_state.config(text='Current state: Idle')
        self.sim_continue_flag = 1
        self.button_pause.config(image=self.photo_list[1])
        self.update_sim_buttons_state(self.sim_start_flag, self.sim_continue_flag)

    def pause_continue_button_pushed(self):
        if self.sim_start_flag == 1:
            if self.sim_continue_flag == 1:
                self.sim_continue_flag = 0
                self.button_pause.config(image=self.photo_list[2])
                self.text_state.config(text='Current state: Running (Paused)')
            else:
                self.sim_continue_flag = 1
                self.button_pause.config(image=self.photo_list[1])
                self.text_state.config(text='Current state: Running')
            self.update_sim_buttons_state(self.sim_start_flag, self.sim_continue_flag)

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

    def close_sim_buttons_frame(self):
        self.draggable_window.place_forget()

    def open_sim_buttons_frame(self):
        self.draggable_window.place(x=175, y=20)

    def on_enter(self, event):
        self.button_x.configure(background='red')

    def on_leave(self, event):
        self.button_x.configure(background=self.background_default_color)
