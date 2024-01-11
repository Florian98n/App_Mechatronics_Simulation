import tkinter as tk
import Simulation_Buttons_File
import Change_Workspace_Size_File


class MenuBar:
    def __init__(self, root, update_rectangle_canvas, update_sim_buttons_state):
        self.sim_buttons = 0
        self.root = root
        self.menubar = tk.Menu(root)

        # Create first dropdown menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=lambda: print("New"))
        self.file_menu.add_command(label="Open")
        self.file_menu.add_command(label="Save")
        # self.file_menu.add_separator()
        # self.file_menu.add_command(label="Exit", command=root.quit)

        # Create second dropdown menu
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Window", menu=self.edit_menu)
        self.edit_menu.add_command(label="Sim Buttons", command=lambda: self.create_sim_buttons_frame())
        self.sim_buttons = Simulation_Buttons_File.SimulationButtons(self.root, update_sim_buttons_state)
        self.edit_menu.add_command(label="Workspace size", command=lambda: self.create_change_workspace_size_frame())
        self.change_workspace_size = Change_Workspace_Size_File.WorkspaceSizeFrame(self.root, update_rectangle_canvas)

        self.root.config(menu=self.menubar)

    def create_change_workspace_size_frame(self):
        self.change_workspace_size.open_workspace_change_size_frame()

    def create_sim_buttons_frame(self):
        self.sim_buttons.open_sim_buttons_frame()
