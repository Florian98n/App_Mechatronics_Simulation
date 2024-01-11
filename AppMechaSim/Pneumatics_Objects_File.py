from PIL import ImageTk, Image
import tkinter as tk


class PneumaticsObject:
    def __init__(self, event, canvas, photo, type_photo, index_photo, index_number, count_zoom, rectangle_canvas):
        self.canvas = canvas
        event.x = int(event.x)
        event.y = int(event.y)
        self.rectangle_canvas = rectangle_canvas
        self.photo = photo
        self.empty_photo = None
        self.last_width = self.photo.width
        self.last_height = self.photo.height
        self.position_x_init = 0  # will be modified by fit_xy_inside_workspace
        self.position_y_init = 0  # will be modified by fit_xy_inside_workspace
        self.position_x_init, self.position_y_init = self.fit_xy_inside_workspace(event, count_zoom, 1)
        self.last_position_x = 0
        self.last_position_y = 0
        self.size_controls = 50
        self.last_size_controls = 50  # default value for calculation of bounding boxes of controls
        self.rectangle = None  # store green rectangle moved with the object
        self.count_zoom = 0  # used at moving object
        self.element_type = type_photo
        self.element_index = index_photo  # 4 for 2/2, 5 for 3/2, 6 for 5/3
        self.element_number = index_number  # index number of element(new element => index+1)
        self.tk_photo = 0
        self.image_id = 0
        self.flag_left_control = [0] * 6
        self.flag_right_control = [0] * 6
        self.tag_name_left = "empty"
        self.tag_name_right = "empty"
        self.left_manual_control_id_image = None
        self.right_manual_control_id_image = None
        self.left_chamber_active = 0                     # always left position is initial position
        self.simulation_mode = 0
        if self.element_index == 4 or self.element_index == 5:
            self.index_shift = 3
        if self.element_index == 6:
            self.index_shift = 4
        self.shift_left = 0

        self.init_flag = 1
        self.zoom_image(count_zoom)
        self.init_flag = 0

    def start_simulation(self):
        self.simulation_mode = 1
        if self.element_index == 4 or self.element_index == 5 or self.element_index == 6:
            empty_image = Image.new("RGBA", (self.last_size_controls, self.last_size_controls), (0, 0, 0, 0))
            self.empty_photo = ImageTk.PhotoImage(empty_image)
            if self.flag_left_control[0] == 1:
                if self.flag_left_control[3] == 1:
                    self.tag_name_left = str(self.element_type)+str(self.element_index)+str(self.element_number)+"left"

                    self.left_manual_control_id_image = self.canvas.create_image(self.last_position_x - self.last_size_controls*self.index_shift,
                                                                                 self.last_position_y,
                                                                                 image=self.empty_photo,
                                                                                 tag=self.tag_name_left, anchor='nw')
                    self.canvas.tag_bind(self.tag_name_left, "<Enter>", lambda event: self.check_hand_enter_left())
                    self.canvas.tag_bind(self.tag_name_left, "<Button-1>", lambda event: self.on_left_side_click())
                    self.canvas.tag_bind(self.tag_name_left, "<Leave>", lambda event: self.check_hand_leave_left())
            if self.flag_right_control[0] == 1:
                if self.flag_right_control[3] == 1:
                    self.tag_name_right = str(self.element_type)+str(self.element_index)+str(self.element_number)+"right"
                    self.right_manual_control_id_image = self.canvas.create_image(self.last_position_x + self.last_size_controls*self.index_shift,
                                                                                  self.last_position_y,
                                                                                  image=self.empty_photo,
                                                                                  tag=self.tag_name_right, anchor='ne')
                    self.canvas.tag_bind(self.tag_name_right, "<Enter>", lambda event: self.check_hand_enter_right())
                    if self.element_index == 6:
                        self.canvas.tag_bind(self.tag_name_right, "<Button-1>", lambda event: self.on_right_side_click())
                    self.canvas.tag_bind(self.tag_name_right, "<Leave>", lambda event: self.check_hand_leave_right())

    def on_left_side_click(self):
        if self.element_index == 4 or self.element_index == 5 or self.element_index == 6:
            self.check_hand_leave_left()
            self.canvas.tag_unbind(self.tag_name_left, "<Button-1>")
            if self.left_chamber_active == 0 or self.element_index == 6:
                self.canvas.delete(self.image_id)
                self.image_id = self.canvas.create_image(self.last_position_x + self.last_size_controls*2,
                                                         self.last_position_y,
                                                         image=self.tk_photo,
                                                         tags=("clickable",
                                                               str(self.element_index),
                                                               str(self.element_number),
                                                               str(self.last_position_x - self.last_width / 2),
                                                               str(self.last_position_y - self.last_height / 2),
                                                               str(self.last_position_x + self.last_width / 2),
                                                               str(self.last_position_y + self.last_height / 2),
                                                               str(self.element_type)))
                self.canvas.delete(self.left_manual_control_id_image)
                self.canvas.delete(self.right_manual_control_id_image)
                if self.element_index == 4 or self.element_index == 5:
                    self.left_manual_control_id_image = self.canvas.create_image(
                        self.last_position_x - self.last_size_controls,
                        self.last_position_y,
                        image=self.empty_photo, tag=self.tag_name_left,
                        anchor='nw')
                    if self.flag_right_control[3] == 1:
                        self.right_manual_control_id_image = self.canvas.create_image(
                            self.last_position_x + self.last_size_controls*5,
                            self.last_position_y,
                            image=self.empty_photo, tag=self.tag_name_right,
                            anchor='ne')
                        self.canvas.tag_bind(self.tag_name_right, "<Button-1>", lambda event: self.on_right_side_click())
                if self.element_index == 6:
                    self.canvas.bind("<ButtonRelease-1>", self.on_left_release)
            self.left_chamber_active = 1

    def on_right_side_click(self):
        if self.element_index == 4 or self.element_index == 5 or self.element_index == 6:
            self.check_hand_leave_right()
            self.canvas.tag_unbind(self.tag_name_right, "<Button-1>")
            if self.element_index == 6:
                self.shift_left = 2
            else:
                self.shift_left = 0
            if self.left_chamber_active == 1 or self.element_index == 6:
                self.canvas.delete(self.image_id)
                self.image_id = self.canvas.create_image(self.last_position_x - self.last_size_controls*self.shift_left,
                                                         self.last_position_y,
                                                         image=self.tk_photo,
                                                         tags=("clickable",
                                                               str(self.element_index),
                                                               str(self.element_number),
                                                               str(self.last_position_x - self.last_width / 2),
                                                               str(self.last_position_y - self.last_height / 2),
                                                               str(self.last_position_x + self.last_width / 2),
                                                               str(self.last_position_y + self.last_height / 2),
                                                               str(self.element_type)))
                self.canvas.delete(self.left_manual_control_id_image)
                self.canvas.delete(self.right_manual_control_id_image)
                if self.element_index == 4 or self.element_index == 5:
                    self.left_manual_control_id_image = self.canvas.create_image(
                        self.last_position_x - self.last_size_controls*3,
                        self.last_position_y,
                        image=self.empty_photo, tag=self.tag_name_left,
                        anchor='nw')
                    if self.flag_left_control[3] == 1:
                        self.right_manual_control_id_image = self.canvas.create_image(
                            self.last_position_x + self.last_size_controls*3,
                            self.last_position_y,
                            image=self.empty_photo, tag=self.tag_name_right,
                            anchor='ne')
                        self.canvas.tag_bind(self.tag_name_left, "<Button-1>", lambda event: self.on_left_side_click())
                if self.element_index == 6:
                    self.canvas.bind("<ButtonRelease-1>", self.on_left_release)
            self.left_chamber_active = 0

    def on_left_release(self, event):
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.delete(self.image_id)
        self.image_id = self.canvas.create_image(self.last_position_x,
                                                 self.last_position_y,
                                                 image=self.tk_photo,
                                                 tags=("clickable",
                                                       str(self.element_index),
                                                       str(self.element_number),
                                                       str(self.last_position_x - self.last_width / 2),
                                                       str(self.last_position_y - self.last_height / 2),
                                                       str(self.last_position_x + self.last_width / 2),
                                                       str(self.last_position_y + self.last_height / 2),
                                                       str(self.element_type)))
        self.start_simulation()

    def stop_simulation(self):
        self.canvas.tag_unbind(self.tag_name_left, "<Enter>")
        self.canvas.tag_unbind(self.tag_name_left, "<Leave>")
        self.canvas.tag_unbind(self.tag_name_right, "<Enter>")
        self.canvas.tag_unbind(self.tag_name_right, "<Leave>")
        self.canvas.tag_unbind(self.tag_name_left, "<Button-1>")
        self.canvas.tag_unbind(self.tag_name_right, "<Button-1>")
        self.canvas.delete(self.left_manual_control_id_image)
        self.left_chamber_active = 0
        self.canvas.delete(self.right_manual_control_id_image)
        self.zoom_image(self.count_zoom)
        self.simulation_mode = 0

    def check_hand_enter_left(self):
        self.canvas.config(cursor="hand2")

    def check_hand_leave_left(self):
        self.canvas.config(cursor="")

    def check_hand_enter_right(self):
        self.canvas.config(cursor="hand2")

    def check_hand_leave_right(self):
        self.canvas.config(cursor="")

    def update_photo_inside_new_workspace(self, count_zoom):
        my_event = Temp(self.last_position_x,
                        self.last_position_y)  # this event is related with workspace, not with view
        self.position_x_init, self.position_y_init = self.fit_xy_inside_workspace(my_event, count_zoom, 0)
        if count_zoom == 1:
            self.position_x_init = self.position_x_init / 2
            self.position_y_init = self.position_y_init / 2
        if count_zoom == -1:
            self.position_x_init = self.position_x_init * 2
            self.position_y_init = self.position_y_init * 2
        if count_zoom == -2:
            self.position_x_init = self.position_x_init * 4
            self.position_y_init = self.position_y_init * 4

    def fit_xy_inside_workspace(self, event, count_zoom, use_adding):
        scrollbar_adding_x1, scrollbar_adding_y1 = self.add_scrollbar_influence()
        # scrollbar_adding_x1, scrollbar_adding_y1 = distance from 0,0 (workspace) until the top left edge of the view
        # scrollbar is needed when the raportation is with the canvas(inside scrollbars)
        # when update image the raportation is with the workspace
        if use_adding == 0:
            scrollbar_adding_x1, scrollbar_adding_y1 = 0, 0
        width_temp = self.photo.width
        height_temp = self.photo.height
        width_photo = width_temp  # I modify recently to self.last_width from self.width
        height_photo = height_temp
        x1, y1, x2, y2 = self.canvas.coords(self.rectangle_canvas)
        if count_zoom == 1:
            width_photo = int(width_temp * 2)
            height_photo = int(height_temp * 2)
        elif count_zoom == -1:
            width_photo = int(width_temp / 2)
            height_photo = int(height_temp / 2)
        elif count_zoom == -2:
            width_photo = int(width_temp / 4)
            height_photo = int(height_temp / 4)
        # If the canvas is just zoomed then the object can't go in left
        # and can go in right until the end of canvas (even without window)
        # x1 = the left edge of the canvas
        # x2 = the right edge of the canvas
        # If the scrollbar is moved than the window in witch the object needs to move
        # is shifted with scrollbar_adding_x1 points in left
        if event.x < (x1 - scrollbar_adding_x1 + width_photo / 2):
            position_x = x1 - scrollbar_adding_x1 + width_photo / 2
        elif event.x > (x2 - scrollbar_adding_x1 - width_photo / 2):
            position_x = x2 - scrollbar_adding_x1 - width_photo / 2
        else:
            position_x = event.x
        if event.y < (y1 - scrollbar_adding_y1 + height_photo / 2):
            position_y = y1 - scrollbar_adding_y1 + height_photo / 2
        elif event.y > (y2 - scrollbar_adding_y1 - height_photo / 2):
            position_y = y2 - scrollbar_adding_y1 - height_photo / 2
        else:
            position_y = event.y
        position_x, position_y = position_x + scrollbar_adding_x1, position_y + scrollbar_adding_y1
        return position_x, position_y

    def add_scrollbar_influence(self):
        x1_percent_left, x2_percent_right = self.canvas.xview()
        y1_percent_up, y2_percent_down = self.canvas.yview()
        x1, y1, x2, y2 = self.canvas.coords(self.rectangle_canvas)
        add_x1 = x1_percent_left * (x2 - x1)
        add_y1 = y1_percent_up * (y2 - y1)
        return add_x1, add_y1

    def make_movable(self, count_zoom, rectangle):
        self.count_zoom = count_zoom
        self.rectangle = rectangle
        self.canvas.tag_bind(self.image_id, '<ButtonPress-1>', self.start_drag)
        self.canvas.tag_bind(self.image_id, '<ButtonRelease-1>', self.stop_drag)
        self.canvas.tag_bind(self.image_id, '<B1-Motion>', self.do_drag)

    def start_drag(self, event):
        x = 1  # nothing but the function needs to exist

    def do_drag(self, event):
        mouse_x, mouse_y = self.fit_xy_inside_workspace(event, self.count_zoom, 1)
        dx = mouse_x - self.last_position_x
        dy = mouse_y - self.last_position_y
        self.canvas.move(self.image_id, dx, dy)
        self.canvas.move(self.rectangle, dx, dy)  # move rectangle
        self.last_position_x = mouse_x
        self.last_position_y = mouse_y

    def stop_drag(self, event):
        self.canvas.delete(self.rectangle)  # delete rectangle
        self.canvas.tag_unbind(self.image_id, '<ButtonPress-1>')
        self.canvas.tag_unbind(self.image_id, '<ButtonRelease-1>')
        self.canvas.tag_unbind(self.image_id, '<B1-Motion>')
        self.position_x_init = int(self.last_position_x)
        self.position_y_init = int(self.last_position_y)
        self.init_flag = 1
        self.zoom_image(self.count_zoom)
        self.init_flag = 0

    def zoom_image(self, count_zoom):
        width = self.photo.width
        height = self.photo.height
        position_x = self.position_x_init
        position_y = self.position_y_init
        size = self.size_controls
        if count_zoom == 1:
            width = width * 2
            height = height * 2
            size = size * 2
            if self.init_flag:
                self.position_x_init = int(self.position_x_init / 2)
                self.position_y_init = int(self.position_y_init / 2)
            else:
                position_x = int(position_x * 2)
                position_y = int(position_y * 2)
        if count_zoom == -1:
            width = width / 2
            height = height / 2
            size = size / 2
            if self.init_flag:
                self.position_x_init = int(self.position_x_init * 2)
                self.position_y_init = int(self.position_y_init * 2)
            else:
                position_x = int(position_x / 2)
                position_y = int(position_y / 2)
        if count_zoom == -2:
            width = width / 4
            height = height / 4
            size = size / 4
            if self.init_flag:
                self.position_x_init = int(self.position_x_init * 4)
                self.position_y_init = int(self.position_y_init * 4)
            else:
                position_x = int(position_x / 4)
                position_y = int(position_y / 4)
        self.last_position_x = position_x
        self.last_position_y = position_y
        self.last_width = int(width)
        self.last_height = int(height)
        self.last_size_controls = int(size)
        self.tk_photo = ImageTk.PhotoImage(self.photo.resize((self.last_width, self.last_height)))
        self.canvas.delete(self.image_id)
        self.image_id = self.canvas.create_image(self.last_position_x,
                                                 self.last_position_y,
                                                 image=self.tk_photo,
                                                 tags=("clickable",
                                                       str(self.element_index),
                                                       str(self.element_number),
                                                       str(self.last_position_x - self.last_width / 2),
                                                       str(self.last_position_y - self.last_height / 2),
                                                       str(self.last_position_x + self.last_width / 2),
                                                       str(self.last_position_y + self.last_height / 2),
                                                       str(self.element_type)))
        if self.simulation_mode == 1:
            empty_image = Image.new("RGBA", (self.last_size_controls, self.last_size_controls), (0, 0, 0, 0))
            self.empty_photo = ImageTk.PhotoImage(empty_image)
            self.canvas.tag_unbind(self.tag_name_left, "<Button-1>")
            self.canvas.tag_unbind(self.tag_name_right, "<Button-1>")
            self.canvas.delete(self.left_manual_control_id_image)
            self.canvas.delete(self.right_manual_control_id_image)

            if self.left_chamber_active == 1:
                self.left_chamber_active = 0
                self.on_left_side_click()
                self.left_manual_control_id_image = self.canvas.create_image(
                    self.last_position_x,
                    self.last_position_y,
                    image=self.empty_photo, tag=self.tag_name_left,
                    anchor='nw')
                self.right_manual_control_id_image = self.canvas.create_image(
                    self.last_position_x + self.last_width,
                    self.last_position_y,
                    image=self.empty_photo, tag=self.tag_name_right,
                    anchor='ne')
            else:
                self.left_manual_control_id_image = self.canvas.create_image(
                    self.last_position_x - int(self.last_width / 2),
                    self.last_position_y,
                    image=self.empty_photo, tag=self.tag_name_left,
                    anchor='nw')
                self.right_manual_control_id_image = self.canvas.create_image(
                    self.last_position_x + int(self.last_width / 2),
                    self.last_position_y,
                    image=self.empty_photo, tag=self.tag_name_left,
                    anchor='ne')
            self.canvas.tag_bind(self.tag_name_left, "<Button-1>", lambda event: self.on_left_side_click())
            self.canvas.tag_bind(self.tag_name_right, "<Button-1>", lambda event: self.on_right_side_click())


class Temp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
