from PIL import Image, ImageTk
import tkinter as tk
import Photos_File


class ParametersFile(tk.Toplevel):
    def __init__(self, label, photo_type, photo_index, send_data_from_parameters, flag_left_control, flag_right_control, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, *kwargs)
        self.root = self
        self.title("Parameters for: " + label)
        self.geometry("700x300")
        self.resizable(False, False)
        self.grab_set()

        self.height_image_type = None       # 0 for spring + 50*50, 50 for 50*50
        self.photo_index = int(photo_index)
        self.send_data_from_parameters = send_data_from_parameters
        if photo_type == '0':
            self.main_photo = Photos_File.p_a_photos[int(photo_index)]
        elif photo_type == '1':
            self.main_photo = Photos_File.p_p_photos[int(photo_index)]
        else:
            self.main_photo = Photos_File.p_f_photos[int(photo_index)]
        self.new_photo = self.main_photo
        self.tk_photo = ImageTk.PhotoImage(self.main_photo)
        self.flag_left_control = [0]*6
        # [0]=0 is if no left control
        # [0]=1 there is left control
        # [3]=1 left control mechanical(only one left control)
        self.flag_right_control = [0]*6
        self.left_control_image = None
        self.right_control_image = None
        self.label = tk.Label(self.root, image=self.tk_photo)
        self.label.place(x=350, y=150, anchor='center')

        self.button_save = tk.Button(self, text="Save", width=8, command=lambda: self.save_new_image())
        self.button_save.place(x=350, y=270, anchor='center')
        self.default_background = self.button_save['bg']
        if self.photo_index == 4 or self.photo_index == 5:  # valve 2/2 and valve 3/2
            self.height_image_type = 50
            self.buttons = [tk.Button] * 12
            self.buttons[0] = tk.Button(self, text="None", width=12, command=lambda: self.press_button(0))
            self.buttons[0].place(x=5, y=40)
            self.buttons[1] = tk.Button(self, text="Spring", width=12, command=lambda: self.press_button(1))
            self.buttons[1].place(x=5, y=80)
            self.buttons[2] = tk.Button(self, text="Mechanical", width=12, command=lambda: self.press_button(2))
            self.buttons[2].place(x=5, y=120)
            self.buttons[3] = tk.Button(self, text="Manual", width=12, command=lambda: self.press_button(3))
            self.buttons[3].place(x=5, y=160)
            self.buttons[4] = tk.Button(self, text="Pneumatic", width=12, command=lambda: self.press_button(4))
            self.buttons[4].place(x=5, y=200)
            self.buttons[5] = tk.Button(self, text="Electric", width=12, command=lambda: self.press_button(5))
            self.buttons[5].place(x=5, y=240)
            self.buttons[6] = tk.Button(self, text="None", width=12, command=lambda: self.press_button(6))
            self.buttons[6].place(x=695, y=40, anchor='ne')
            self.buttons[7] = tk.Button(self, text="Spring", width=12, command=lambda: self.press_button(7))
            self.buttons[7].place(x=695, y=80, anchor='ne')
            self.buttons[8] = tk.Button(self, text="Mechanical", width=12, command=lambda: self.press_button(8))
            self.buttons[8].place(x=695, y=120, anchor='ne')
            self.buttons[9] = tk.Button(self, text="Manual", width=12, command=lambda: self.press_button(9))
            self.buttons[9].place(x=695, y=160, anchor='ne')
            self.buttons[10] = tk.Button(self, text="Pneumatic", width=12, command=lambda: self.press_button(10))
            self.buttons[10].place(x=695, y=200, anchor='ne')
            self.buttons[11] = tk.Button(self, text="Electric", width=12, command=lambda: self.press_button(11))
            self.buttons[11].place(x=695, y=240, anchor='ne')

        if self.photo_index == 6:
            self.height_image_type = 0  # the images are inserted at height 0 because they have height 100
            self.buttons = [tk.Button] * 12
            self.buttons[0] = tk.Button(self, text="None", width=16, background="#92FF8E",
                                        command=lambda: self.press_button(0))
            self.buttons[0].place(x=5, y=40)
            self.buttons[1] = tk.Button(self, text="Spring", width=16, command=lambda: self.press_button(1))
            self.buttons[1].place(x=5, y=80)
            self.buttons[2] = tk.Button(self, text="Spring Mechanical", width=16, command=lambda: self.press_button(2))
            self.buttons[2].place(x=5, y=120)
            self.buttons[3] = tk.Button(self, text="Spring Manual", width=16, command=lambda: self.press_button(3))
            self.buttons[3].place(x=5, y=160)
            self.buttons[4] = tk.Button(self, text="Spring Pneumatic", width=16, command=lambda: self.press_button(4))
            self.buttons[4].place(x=5, y=200)
            self.buttons[5] = tk.Button(self, text="Spring Electric", width=16, command=lambda: self.press_button(5))
            self.buttons[5].place(x=5, y=240)
            self.buttons[6] = tk.Button(self, text="None", width=16, background="#92FF8E",
                                        command=lambda: self.press_button(6))
            self.buttons[6].place(x=695, y=40, anchor='ne')
            self.buttons[7] = tk.Button(self, text="Spring", width=16, command=lambda: self.press_button(7))
            self.buttons[7].place(x=695, y=80, anchor='ne')
            self.buttons[8] = tk.Button(self, text="Spring Mechanical", width=16, command=lambda: self.press_button(8))
            self.buttons[8].place(x=695, y=120, anchor='ne')
            self.buttons[9] = tk.Button(self, text="Spring Manual", width=16, command=lambda: self.press_button(9))
            self.buttons[9].place(x=695, y=160, anchor='ne')
            self.buttons[10] = tk.Button(self, text="Spring Pneumatic", width=16, command=lambda: self.press_button(10))
            self.buttons[10].place(x=695, y=200, anchor='ne')
            self.buttons[11] = tk.Button(self, text="Spring Electric", width=16, command=lambda: self.press_button(11))
            self.buttons[11].place(x=695, y=240, anchor='ne')
        if flag_left_control[0] == 0:
            self.press_button(0)
        else:
            for index in range(1, len(self.flag_left_control)):
                if flag_left_control[index] == 1:
                    self.press_button(index)
        if flag_right_control[0] == 0:
            self.press_button(6)
        else:
            for index in range(1, len(self.flag_right_control)):
                if flag_right_control[index] == 1:
                    self.press_button(index + 6)

    def save_new_image(self):
        self.send_data_from_parameters(self.new_photo, self.flag_left_control, self.flag_right_control)
        self.root.destroy()

    def update_photo(self):
        if self.flag_left_control[0] and self.flag_right_control[0]:
            self.new_photo = Image.new("RGBA", (50 + self.main_photo.width + 50, self.main_photo.height),
                                       (0, 0, 0, 0))
            self.new_photo.paste(self.left_control_image, (0, self.height_image_type))
            self.new_photo.paste(self.main_photo, (50, 0))
            self.new_photo.paste(self.right_control_image, (50 + self.main_photo.width, self.height_image_type))
        elif self.flag_left_control[0] and self.flag_right_control[0] == 0:
            self.new_photo = Image.new("RGBA", (50 + self.main_photo.width, self.main_photo.height),
                                       (0, 0, 0, 0))
            self.new_photo.paste(self.left_control_image, (0, self.height_image_type))
            self.new_photo.paste(self.main_photo, (50, 0))
        elif self.flag_left_control[0] == 0 and self.flag_right_control[0]:
            self.new_photo = Image.new("RGBA", (self.main_photo.width + 50, self.main_photo.height),
                                       (0, 0, 0, 0))
            self.new_photo.paste(self.main_photo, (0, 0))
            self.new_photo.paste(self.right_control_image, (self.main_photo.width, self.height_image_type))
        else:
            self.new_photo = self.main_photo
        self.tk_photo = ImageTk.PhotoImage(self.new_photo)
        self.label.config(image=self.tk_photo)

    def press_button(self, index):
        if index < 6:
            start_indexing = 0
        else:
            start_indexing = 6
        for i in range(start_indexing, start_indexing + 6):
            if i == index:
                self.buttons[i].configure(background="#92FF8E")
            else:
                self.buttons[i].configure(background=self.default_background)
        if index == 0:
            self.flag_left_control[0] = 0
        elif 0 < index < 6:
            self.flag_left_control = [0 for _ in self.flag_left_control]
            self.flag_left_control[0] = 1
            self.flag_left_control[index] = 1
            self.left_control_image = Photos_File.list_controls[self.photo_index-4][index]
        if index == 6:
            self.flag_right_control[0] = 0
        elif 6 < index < 12:
            self.flag_right_control = [0 for _ in self.flag_right_control]
            self.flag_right_control[0] = 1
            self.flag_right_control[index-6] = 1
            self.right_control_image = Photos_File.list_controls[self.photo_index-4][index]
        self.update_photo()
