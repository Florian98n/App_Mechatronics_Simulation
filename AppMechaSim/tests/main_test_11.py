import tkinter as tk

class Main(tk.Tk):

    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self,*args, *kwargs)

        self.button = tk.Button(self,text="second window", command=lambda: SecondWindow())
        self.button.pack()


class SecondWindow(tk.Toplevel):

    def __init__(self,*args, **kwargs):
        tk.Toplevel.__init__(self,*args, *kwargs)
        self.button = tk.Button(self,text="quit", command=lambda: quit())
        self.button.pack()
        self.grab_set()

if __name__ == "__main__":
    app = Main()
    app.mainloop()