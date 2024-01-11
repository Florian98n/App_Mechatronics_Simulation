import tkinter as tk
import PIL
from PIL import Image, ImageTk
import Photos_File


class Buttons:
    def __init__(self, frame, workspace_add_object, workspace_erase_object):
        self.frame = frame
        self.workspace_add_object = workspace_add_object
        self.workspace_erase_object = workspace_erase_object
        self.flag_button_pushed = 0
        self.index = 0
        self.last_main_button_type = 0
        self.last_button_type = 0
        self.last_button_index = 0
        self.show_main_buttons_var = [1]*3
        self.show_p_sub_vars = [1] * 3
        self.show_h_sub_vars = [1] * 3
        self.show_e_sub_vars = [1] * 3
        self.show_list_sub_vars = [self.show_p_sub_vars, self.show_h_sub_vars, self.show_e_sub_vars]

        self.buttons = [tk.Button] * 3  # Pneumatics, Hydraulics, Electronics
        self.buttons[0] = tk.Button(self.frame, anchor='w', text="+ Pneumatics", width=17, command=lambda: self.flip_main_button(0), takefocus=False)
        self.buttons[1] = tk.Button(self.frame, anchor='w', text="+ Hydraulics", width=17, takefocus=False, command=lambda: self.flip_main_button(1))
        self.buttons[2] = tk.Button(self.frame, anchor='w', text="+ Electronics", width=17, takefocus=False, command=lambda: self.flip_main_button(2))
        self.buttons[0].pack()
        self.buttons[1].pack()
        self.buttons[2].pack()

        self.buttons_pne = [[tk.Button(self.frame) for _ in range(Photos_File.p_a_nr_elements)]]      # Active
        self.buttons_pne.append([tk.Button(self.frame) for _ in range(Photos_File.p_p_nr_elements)])  # Passive
        self.buttons_pne.append([tk.Button(self.frame) for _ in range(Photos_File.p_f_nr_elements)])  # FRL

        # Active, cylinder1, cylinder2, cylinder3, valve 2/2, valve 3/2, valve 5/3, compressor
        self.p_a_photos_buttons = [ImageTk.PhotoImage] * Photos_File.p_a_nr_elements
        self.p_a_photos_buttons[0] = None
        self.p_a_photos_buttons[1] = ImageTk.PhotoImage(Photos_File.p_a_buttons[1])
        self.p_a_photos_buttons[2] = ImageTk.PhotoImage(Photos_File.p_a_buttons[2])
        self.p_a_photos_buttons[3] = ImageTk.PhotoImage(Photos_File.p_a_buttons[3])
        self.p_a_photos_buttons[4] = ImageTk.PhotoImage(Photos_File.p_a_buttons[4])
        self.p_a_photos_buttons[5] = ImageTk.PhotoImage(Photos_File.p_a_buttons[5])
        self.p_a_photos_buttons[6] = ImageTk.PhotoImage(Photos_File.p_a_buttons[6])
        self.p_a_photos_buttons[7] = ImageTk.PhotoImage(Photos_File.p_a_buttons[7])
        self.buttons_pne[0][0] = tk.Button(self.frame, anchor='w', text="     + Active", takefocus=False, command=lambda: self.flip_button(0, 0))
        self.buttons_pne[0][1] = tk.Button(self.frame, anchor='center', width=130, image=self.p_a_photos_buttons[1],
                                           text="Cylinder single acting", compound='bottom', takefocus=False,
                                           command=lambda: self.push_button(0, 0, 1))
        self.buttons_pne[0][2] = tk.Button(self.frame, anchor='center', width=130, image=self.p_a_photos_buttons[2],
                                           text="Cylinder double acting", compound='bottom', takefocus=False,
                                           command=lambda: self.push_button(0, 0, 2))
        self.buttons_pne[0][3] = tk.Button(self.frame, anchor='center', width=130, image=self.p_a_photos_buttons[3],
                                           text="Cylinder single acting", compound='bottom', takefocus=False,
                                           command=lambda: self.push_button(0, 0, 3))
        self.buttons_pne[0][4] = tk.Button(self.frame, anchor='center', width=130, image=self.p_a_photos_buttons[4],
                                           text="Valve 2/2", compound='bottom', takefocus=False,
                                           command=lambda: self.push_button(0, 0, 4))
        self.buttons_pne[0][5] = tk.Button(self.frame, anchor='center', width=130, image=self.p_a_photos_buttons[5],
                                           text="Valve 3/2", compound='bottom', takefocus=False,
                                           command=lambda: self.push_button(0, 0, 5))
        self.buttons_pne[0][6] = tk.Button(self.frame, anchor='center', width=130, image=self.p_a_photos_buttons[6],
                                           text="Valve 5/3", compound='bottom', takefocus=False,
                                           command=lambda: self.push_button(0, 0, 6))
        self.buttons_pne[0][7] = tk.Button(self.frame, anchor='center', width=130, image=self.p_a_photos_buttons[7],
                                           text="Compressor", compound='bottom', takefocus=False,
                                           command=lambda: self.push_button(0, 0, 7))

        #  Passive, Check valve, Muffler
        self.p_p_photos_buttons = [ImageTk.PhotoImage] * Photos_File.p_p_nr_elements
        self.p_p_photos_buttons[0] = None
        self.p_p_photos_buttons[1] = ImageTk.PhotoImage(Photos_File.p_p_buttons[1])
        self.p_p_photos_buttons[2] = ImageTk.PhotoImage(Photos_File.p_p_buttons[2])
        self.buttons_pne[1][0] = tk.Button(self.frame, anchor='w', text="     + Passive", takefocus=False, command=lambda: self.flip_button(0, 1))
        self.buttons_pne[1][1] = tk.Button(self.frame, anchor='center', width=130, image=self.p_p_photos_buttons[1],
                                           text="Check valve", compound='bottom', takefocus=False,
                                           command=lambda: self.push_button(0, 1, 1))
        self.buttons_pne[1][2] = tk.Button(self.frame, anchor='center', width=130, image=self.p_p_photos_buttons[2],
                                           text="Muffler", compound='bottom', takefocus=False,
                                           command=lambda: self.push_button(0, 1, 2))

        # FRL, Regulator
        self.p_f_photos_buttons = [ImageTk.PhotoImage] * Photos_File.p_f_nr_elements
        self.p_f_photos_buttons[0] = None
        self.p_f_photos_buttons[1] = ImageTk.PhotoImage(Photos_File.p_f_buttons[1])
        self.buttons_pne[2][0] = tk.Button(self.frame, anchor='w', text="     + FRL", takefocus=False, command=lambda: self.flip_button(0, 2))
        self.buttons_pne[2][1] = tk.Button(self.frame, anchor='center', width=130, image=self.p_f_photos_buttons[1],
                                           text="Regulator", compound='bottom', takefocus=False,
                                           command=lambda: self.push_button(0, 2, 1))

        self.buttons_hyd = [[tk.Button(self.frame) for _ in range(1)]]  # Active
        self.buttons_hyd.append([tk.Button(self.frame) for _ in range(1)])  # Passive
        self.buttons_hyd.append([tk.Button(self.frame) for _ in range(1)])  # FRL

        # Active, Passive, FRL
        self.buttons_hyd[0][0] = tk.Button(self.frame, anchor='w', text="     + Active", takefocus=False, command=lambda: self.flip_button(1, 0))
        self.buttons_hyd[1][0] = tk.Button(self.frame, anchor='w', text="     + Passive", takefocus=False, command=lambda: self.flip_button(1, 1))
        self.buttons_hyd[2][0] = tk.Button(self.frame, anchor='w', text="     + FRL", takefocus=False, command=lambda: self.flip_button(1, 2))

        self.buttons_ele = [[tk.Button(self.frame) for _ in range(1)]]  # Active
        self.buttons_ele.append([tk.Button(self.frame) for _ in range(1)])  # Passive
        self.buttons_ele.append([tk.Button(self.frame) for _ in range(6)])  # Ladder

        self.buttons_ele[0][0] = tk.Button(self.frame, anchor='w', text="     + Active", takefocus=False, command=lambda: self.flip_button(2, 0))
        self.buttons_ele[1][0] = tk.Button(self.frame, anchor='w', text="     + Passive", takefocus=False, command=lambda: self.flip_button(2, 1))
        self.buttons_ele[2][0] = tk.Button(self.frame, anchor='w', text="     + Ladder", takefocus=False, command=lambda: self.flip_button(2, 2))
        self.buttons_ele[2][1] = tk.Button(self.frame, anchor='w', text="Coil", takefocus=False)
        self.buttons_ele[2][2] = tk.Button(self.frame, anchor='w', text="Not Coil", takefocus=False)
        self.buttons_ele[2][3] = tk.Button(self.frame, anchor='w', text="Output Coil", takefocus=False)
        self.buttons_ele[2][4] = tk.Button(self.frame, anchor='w', text="Timer", takefocus=False)
        self.buttons_ele[2][5] = tk.Button(self.frame, anchor='w', text="Counter", takefocus=False)

        self.buttons_list = [self.buttons_pne, self.buttons_hyd, self.buttons_ele]

    def push_button(self, main_button_type, button_type, button_index):
        if self.flag_button_pushed == 0:
            self.last_main_button_type = main_button_type
            self.last_button_type = button_type
            self.last_button_index = button_index
            self.flag_button_pushed = 1
            self.buttons_list[self.last_main_button_type][self.last_button_type][self.last_button_index].config(relief=tk.SUNKEN, bd=3)
            self.workspace_add_object(self.last_button_type, self.last_button_index)
        else:
            self.release_button()
            self.workspace_erase_object()

    def release_button(self):
        self.buttons_list[self.last_main_button_type][self.last_button_type][self.last_button_index].config(relief=tk.RAISED, state=tk.NORMAL)
        self.flag_button_pushed = 0

    def search_text(self, text):
        self.hide_buttons()
        temp_list_buttons = [self.buttons_pne, self.buttons_hyd, self.buttons_ele]
        for i in range(0, 3):
            for j in range(0, 3):
                for k in range(1, len(temp_list_buttons[i][j])):
                    if text in temp_list_buttons[i][j][k].cget("text").lower():
                        temp_list_buttons[i][j][k].pack(side="top", fill="x")

    def restore_from_search(self):
        self.hide_buttons()
        self.show_buttons()

    def flip_button(self, button_type, button_index):
        text = None
        self.hide_buttons()
        if button_index == 0:
            text = "Active"
        elif button_index == 1:
            text = "Passive"
        else:
            if button_type == 2:
                text = "Ladder"
            else:
                text = "FRL"
        if self.show_list_sub_vars[button_type][button_index]:
            self.buttons_list[button_type][button_index][0].config(text="     - "+text)
        else:
            self.buttons_list[button_type][button_index][0].config(text="     + " + text)
        self.show_list_sub_vars[button_type][button_index] = 1 - self.show_list_sub_vars[button_type][button_index]
        self.show_buttons()

    def hide_buttons(self):
        self.buttons[0].pack_forget()
        self.buttons[1].pack_forget()
        self.buttons[2].pack_forget()
        for i in range(0, 3):
            for j in range(0, 3):
                for k in range(0, len(self.buttons_list[i][j])):
                    self.buttons_list[i][j][k].pack_forget()

    def show_buttons(self):
        for i in range(0, 3):
            self.buttons[i].pack(side="top", fill="x")
            if self.show_main_buttons_var[i] == 0:
                for j in range(0, 3):
                    self.buttons_list[i][j][0].pack(side="top", fill="x")
                    if self.show_list_sub_vars[i][j] == 0:
                        for k in range(1, len(self.buttons_list[i][j])):
                            self.buttons_list[i][j][k].pack(side="top", fill="x")

    def flip_main_button(self, button_type):
        text = None
        if button_type == 0:
            text = "Pneumatics"
        elif button_type == 1:
            text = "Hydraulics"
        else:
            text = "Electronics"
        self.hide_buttons()
        if self.show_main_buttons_var[button_type]:
            self.buttons[button_type].config(text="- "+text)
        else:
            self.buttons[button_type].config(text="+ "+text)
        self.show_main_buttons_var[button_type] = 1 - self.show_main_buttons_var[button_type]
        self.show_buttons()
