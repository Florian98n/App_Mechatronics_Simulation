import tkinter as tk


class Frames:
    def __init__(self, root):
        self.root = root

        # search addable
        self.frame_search_addable = tk.Frame(self.root, width=150, height=50)
        self.frame_search_addable.place(x=5, y=5)

        # addable list
        self.frame_addable_list = tk.Frame(self.root, width=150, height=50)
        self.frame_addable_list.pack(side='left', padx=(5, 0), pady=(60, 0))

        self.canvas = tk.Canvas(self.frame_addable_list, width=130, height=50)
        self.canvas.pack(side='left', expand=True)

        self.scrollbar = tk.Scrollbar(self.frame_addable_list, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='left', fill='y')
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.button_list_canvas = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.button_list_canvas, anchor='nw')

        # workspace
        self.frame_workspace = (tk.Frame(root, width=100, height=50, bg="white"))
        self.frame_workspace.place(x=160, y=5)

        # control workspace
        #self.frame_workspace = (tk.Frame(root, width=100, height=50, bg="white"))
        #self.frame_workspace.place(x=160, y=5)

    def on_resize(self, event):
        if self.frame_workspace.winfo_exists():
            self.frame_workspace.configure(width=self.root.winfo_width() - 160 - 5)  # - 5 - search width - 5
            self.frame_workspace.configure(height=self.root.winfo_height() - 5 - 5)

            self.canvas.configure(height=self.root.winfo_height() - 5 - 60 - 5 - 5)  # -5 - search height - 5 - 5
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))



