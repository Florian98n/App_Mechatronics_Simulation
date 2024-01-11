import tkinter as tk


class SearchZone:
    def __init__(self, frame, root, search_text, restore_from_search):
        self.frame = frame
        self.root = root
        self.search_text = search_text
        self.restore_from_search = restore_from_search
        self.search_var = tk.StringVar()

        self.entry_search = tk.Entry(self.frame, textvariable=self.search_var)
        self.entry_search.pack()
        self.entry_search.bind('<FocusOut>', self.on_focusout)

        self.search_button = tk.Button(frame, text="Search", width=5, command=self.update_search_buttons)
        self.search_button.pack(side='right', padx=5, pady=5, expand=True)

        self.x_button = tk.Button(self.frame, text="X", width=5, command=self.update_x_buttons)
        self.x_button.pack(side='left', padx=5, pady=5, expand=True)

    def update_search_buttons(self):
        text = self.search_var.get().lower()
        self.search_text(text)

    def update_x_buttons(self):
        self.entry_search.delete(0, tk.END)
        self.restore_from_search()

    def on_focusout(self, event=None):
        self.root.focus()

