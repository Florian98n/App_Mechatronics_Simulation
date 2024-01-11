import tkinter as tk
from PIL import Image, ImageTk


class GlobalButtons:
    def __init__(self, frame):
        self.frame = frame
        self.show_pn_var = 1
        self.show_tr_var = 1
        self.show_hy_var = 1
        self.show_el_var = 1

        self.btn1_pneumatics = tk.Button(self.frame, anchor='w', text=" + Pneumatics", width=20, command=lambda: self.flip_pneumatics())
        self.btn1_pneumatics.pack(side="top", fill="x")
        self.btn11_active = tk.Button(self.frame, anchor='w', text="     + Active")
        self.btn12_transmission = tk.Button(self.frame, anchor='w', text="     + Transmission", command=lambda: self.flip_transmission())
        self.photo1 = ImageTk.PhotoImage(Image.open('valve3_2_.jpg'))
        self.btn121_valve3_2 = tk.Button(self.frame, height=50, anchor='center', image=self.photo1, text="Valve 3/2   ", compound='right')
        self.photo2 = ImageTk.PhotoImage(Image.open('valve4_3.jpg'))
        self.btn122_valve4_3 = tk.Button(self.frame, height=50, anchor='center', image=self.photo2, text="Valve 4/3   ", compound='right')
        self.btn13_passive = tk.Button(self.frame, anchor='w', text="     + Passive")
        self.btn14_frl = tk.Button(self.frame, anchor='w', text="     + FRL")

        self.btn2_hydraulics = tk.Button(self.frame, anchor='w', text=" + Hydraulics", command=lambda: self.flip_hydraulics())
        self.btn2_hydraulics.pack(side="top", fill="x")

        self.btn3_electronics = tk.Button(self.frame, anchor='w', text=" + Electronics", command=lambda: self.flip_electronics())
        self.btn3_electronics.pack(side="top", fill="x")

    def flip_pneumatics(self):
        self.hide_hyd_ele()
        if self.show_pn_var:
            self.btn1_pneumatics.config(text=" - Pneumatics")
            self.show_buttons_pneumatics()
        else:
            self.btn1_pneumatics.config(text=" + Pneumatics")
            self.hide_buttons_pneumatics()
        self.show_pn_var = 1 - self.show_pn_var
        self.show_hyd_ele()

    def hide_hyd_ele(self):
        self.btn2_hydraulics.pack_forget()
        self.btn3_electronics.pack_forget()

    def show_hyd_ele(self):
        self.btn2_hydraulics.pack(side="top", fill="x")
        self.btn3_electronics.pack(side="top", fill="x")

    def show_buttons_pneumatics(self):
        self.btn11_active.pack(side="top", fill="x")
        self.btn12_transmission.pack(side="top", fill="x")
        if self.show_tr_var==0:
            self.show_buttons_transmission()
        else:
            self.hide_buttons_transmission()
        self.btn13_passive.pack(side="top", fill="x")
        self.btn14_frl.pack(side="top", fill="x")

    def hide_buttons_pneumatics(self):
        self.btn11_active.pack_forget()
        self.btn12_transmission.pack_forget()
        self.hide_buttons_transmission()
        self.btn13_passive.pack_forget()
        self.btn14_frl.pack_forget()

    def flip_transmission(self):
        self.btn13_passive.pack_forget()  # functions in the future
        self.btn14_frl.pack_forget()
        self.hide_hyd_ele()
        if self.show_tr_var:
            self.btn12_transmission.config(text="     - Transmission")
            self.show_buttons_transmission()
        else:
            self.btn12_transmission.config(text="     + Transmission")
            self.hide_buttons_transmission()
        self.show_tr_var = 1 - self.show_tr_var
        self.btn13_passive.pack(side="top", fill="x")  # functions in the future
        self.btn14_frl.pack(side="top", fill="x")
        self.show_hyd_ele()

    def show_buttons_transmission(self):
        self.btn121_valve3_2.pack(side="top", fill="x")
        self.btn122_valve4_3.pack(side="top", fill="x")

    def hide_buttons_transmission(self):
        self.btn121_valve3_2.pack_forget()
        self.btn122_valve4_3.pack_forget()


def main():
    root = tk.Tk()
    root.geometry("500x200")
    #root.state("zoomed")
    frame = tk.Frame(root)
    frame.grid(row=0, column=0)

    my_buttons = GlobalButtons(frame)

    root.mainloop()


if __name__ == '__main__':
    main()