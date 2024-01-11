import tkinter as tk
from PIL import Image, ImageTk
import Pneumatics_Objects_File
import Parameters_Window_File
import Photos_File
import MenuBar_File
import Simulation_Buttons_File


class Workspace:
    def __init__(self, root, frame_workspace, frame_buttons):
        self.count_zoom = 0
        self.rectangle = 0
        self.x = 0
        self.y = 0
        self.width_rectangle_canvas = 10
        self.height_rectangle_canvas = 5
        self.current_photo_type = None
        self.current_photo_index = None
        self.current_photo_number = None
        self.parameters_window = None
        self.label = None
        self.flag = 0
        self.prepared_to_move = 0
        self.release_button = None  # function from addable buttons
        self.sim_start_flag = 0  # simulation is not running
        self.sim_continue_flag = 1  # when the simulation will run it will be in continue state
        self.lines = []
        self.root = root
        self.frame_addable_buttons = frame_buttons
        self.frame_workspace = frame_workspace
        self.frame_workspace.pack(fill=tk.BOTH, expand=True)

        self.width_bar = tk.Scrollbar(self.frame_workspace, orient=tk.HORIZONTAL)
        self.width_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.height_bar = tk.Scrollbar(self.frame_workspace, orient=tk.VERTICAL)
        self.height_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = tk.Canvas(self.frame_workspace, bg='#D3D3D3', xscrollcommand=self.width_bar.set,
                                yscrollcommand=self.height_bar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.width_bar.config(command=self.canvas.xview)
        self.height_bar.config(command=self.canvas.yview)
        self.rectangle_canvas = None
        self.rectangle_canvas = self.canvas.create_rectangle(0, 0, self.width_rectangle_canvas * 100,
                                                             self.height_rectangle_canvas * 100, fill="white",
                                                             tags="scale")
        self.create_lines_for_rectangle_canvas(self.width_rectangle_canvas, self.height_rectangle_canvas, 100)

        self.zoom_buttons = tk.Canvas(self.frame_workspace, bg='white')
        self.zoom_buttons.place(x=10, y=300)
        self.zoom_in_button = tk.Button(self.zoom_buttons, text="Zoom in", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT)
        self.zoom_out_button = tk.Button(self.zoom_buttons, text="Zoom out", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.photos_list = [Photos_File.p_a_photos,
                            Photos_File.p_p_photos,
                            Photos_File.p_f_photos]
        self.matrix_p_a_objects = [[] for _ in range(Photos_File.p_a_nr_elements)]
        self.matrix_p_p_objects = [[] for _ in range(Photos_File.p_p_nr_elements)]
        self.matrix_p_f_objects = [[] for _ in range(Photos_File.p_f_nr_elements)]
        self.matrix_p_objects = [self.matrix_p_a_objects, self.matrix_p_p_objects, self.matrix_p_f_objects]
        self.type_object = 0  # 0 is active
        self.index_object = 0  # the object type 4 is valve 2/2
        self.index_matrix_p_a_objects = [-1] * Photos_File.p_a_nr_elements  # [0] = 1 => two objects type 0
        self.index_matrix_p_p_objects = [-1] * Photos_File.p_p_nr_elements  # [0] = 1 => two objects type 0
        self.index_matrix_p_f_objects = [-1] * Photos_File.p_f_nr_elements  # [0] = 1 => two objects type 0
        self.index_matrix_p_objects = [self.index_matrix_p_a_objects,
                                       self.index_matrix_p_p_objects,
                                       self.index_matrix_p_f_objects]
        self.list_erased_positions_p_a_objects = [[] for _ in range(Photos_File.p_a_nr_elements)]
        self.list_erased_positions_p_p_objects = [[] for _ in range(Photos_File.p_p_nr_elements)]
        self.list_erased_positions_p_f_objects = [[] for _ in range(Photos_File.p_f_nr_elements)]
        self.list_erased_positions_p_objects = [self.list_erased_positions_p_a_objects,
                                                self.list_erased_positions_p_p_objects,
                                                self.list_erased_positions_p_f_objects]

        self.menu = tk.Menu(root, tearoff=0)
        self.canvas.bind('<Button-3>', self.show_menu)

        self.my_menubar = MenuBar_File.MenuBar(self.root, self.update_rectangle_canvas, self.update_sim_buttons_state)

    def update_sim_buttons_state(self, sim_start_flag, sim_continue_flag):
        self.sim_start_flag = sim_start_flag
        if self.sim_start_flag == 1:
            self.canvas.unbind('<Button-3>')
            for widget in self.frame_addable_buttons.winfo_children():
                widget.configure(state='disabled')
            for i in range(0, 3):
                for j in range(0, len(self.matrix_p_objects[i])):
                    for k in range(0, len(self.matrix_p_objects[i][j])):
                        if self.matrix_p_objects[i][j][k] is not None:
                            self.matrix_p_objects[i][j][k].start_simulation()
        else:
            self.canvas.bind('<Button-3>', self.show_menu)
            for widget in self.frame_addable_buttons.winfo_children():
                widget.configure(state='normal')
            for i in range(0, 3):
                for j in range(0, len(self.matrix_p_objects[i])):
                    for k in range(0, len(self.matrix_p_objects[i][j])):
                        if self.matrix_p_objects[i][j][k] is not None:
                            self.matrix_p_objects[i][j][k].stop_simulation()
                            self.matrix_p_objects[i][j][k].zoom_image(self.count_zoom)
        self.sim_continue_flag = sim_continue_flag

    def create_lines_for_rectangle_canvas(self, width_rectangle_canvas, height_rectangle_canvas, step):
        for i in range(1, width_rectangle_canvas, 1):
            temp = self.canvas.create_line(i * step, 0, i * step, height_rectangle_canvas * step, fill='#E6E6E6',
                                           width=1, tags='scale')
            self.lines.append(temp)
        for i in range(1, height_rectangle_canvas, 1):
            temp = self.canvas.create_line(0, i * step, width_rectangle_canvas * step, i * step, fill='#E6E6E6',
                                           width=1, tags='scale')
            self.lines.append(temp)

    def update_rectangle_canvas(self, width_rectangle_canvas, height_rectangle_canvas):
        width_rectangle_canvas = width_rectangle_canvas * 100
        height_rectangle_canvas = height_rectangle_canvas * 100
        step = 100
        self.canvas.coords(self.rectangle_canvas, 0, 0, width_rectangle_canvas, height_rectangle_canvas)
        for i in range(len(self.matrix_p_a_objects)):
            for j in range(len(self.matrix_p_a_objects[i])):
                self.matrix_p_a_objects[i][j].rectangle_canvas = self.rectangle_canvas
        self.width_rectangle_canvas = width_rectangle_canvas
        self.height_rectangle_canvas = height_rectangle_canvas
        if self.count_zoom == 1:
            self.canvas.scale('scale', 0, 0, 2, 2)
            step = step * 2
        elif self.count_zoom == -1:
            self.canvas.scale('scale', 0, 0, 0.5, 0.5)
            step = step / 2
        elif self.count_zoom == -2:
            self.canvas.scale('scale', 0, 0, 0.5, 0.5)
            self.canvas.scale('scale', 0, 0, 0.5, 0.5)
            step = step / 4
        for index in range(0, len(self.lines)):
            self.canvas.delete(self.lines[index])
        self.create_lines_for_rectangle_canvas(int(width_rectangle_canvas / 100),
                                               int(height_rectangle_canvas / 100),
                                               step)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def show_menu(self, event):
        current_item = self.canvas.find_withtag("current")
        if current_item:
            tags = self.canvas.gettags(current_item[0])
            if "clickable" in tags:
                self.menu.delete(0, 2)
                if tags[7] == '0':
                    if tags[1] == '1':
                        self.label = 'Cylinder single acting #'
                    if tags[1] == '2':
                        self.label = 'Cylinder double acting #'
                    if tags[1] == '3':
                        self.label = 'Cylinder double acting #'
                    if tags[1] == '4':
                        self.label = 'Valve 2/2 #'
                    if tags[1] == '5':
                        self.label = 'Valve 3/2 #'
                    if tags[1] == '6':
                        self.label = 'Valve 5/3 #'
                    if tags[1] == '7':
                        self.label = 'Compressor #'
                elif tags[7] == '1':
                    if tags[1] == '1':
                        self.label = 'Check valve #'
                    if tags[1] == '2':
                        self.label = 'Muffler #'
                else:
                    if tags[1] == '1':
                        self.label = 'Regulator #'
                self.label = self.label + tags[2]
                self.current_photo_type = int(tags[7])
                self.current_photo_index = int(tags[1])
                self.current_photo_number = int(tags[2])
                self.menu.add_command(label=self.label, command=lambda: self.create_parameters_window(tags[7], tags[1]))
                self.menu.add_command(label='Move', command=lambda: self.make_movable(int(tags[7]),  # type
                                                                                      int(tags[1]),  # index
                                                                                      int(tags[2]),  # number
                                                                                      tags[3], tags[4], tags[5],
                                                                                      tags[6]))
                self.menu.add_command(label='Delete', command=lambda: self.delete_object(int(tags[7]),
                                                                                         int(tags[1]),
                                                                                         int(tags[2]), ))
                self.menu.post(event.x_root, event.y_root)

    def send_data_from_parameters(self, new_tk_photo, flag_left_control, flag_right_control):
        self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
            self.current_photo_number].flag_left_control = flag_left_control
        self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
            self.current_photo_number].flag_right_control = flag_right_control
        self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
            self.current_photo_number].photo = new_tk_photo
        self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
            self.current_photo_number].width_photo = new_tk_photo.width
        self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
            self.current_photo_number].height_photo = new_tk_photo.height
        self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
            self.current_photo_number].update_photo_inside_new_workspace(self.count_zoom)
        self.matrix_p_objects[self.current_photo_type][self.current_photo_index][self.current_photo_number].zoom_image(
            self.count_zoom)
        self.parameters_window = None

    def create_parameters_window(self, type_photo, index_photo):
        self.parameters_window = Parameters_Window_File.ParametersFile(self.label, type_photo, index_photo,
                                                                       self.send_data_from_parameters,
                                                                       self.matrix_p_objects[
                                                                           self.current_photo_type][
                                                                           self.current_photo_index][
                                                                           self.current_photo_number].flag_left_control,
                                                                       self.matrix_p_objects[
                                                                           self.current_photo_type][
                                                                           self.current_photo_index][
                                                                           self.current_photo_number].flag_right_control)

    def delete_object(self, type_object, index_object, number_object):
        self.matrix_p_objects[type_object][index_object][number_object].canvas.delete(
            self.matrix_p_objects[type_object][index_object][number_object].image_id)
        self.matrix_p_objects[type_object][index_object][number_object] = None
        self.list_erased_positions_p_objects[type_object][index_object].append(number_object)

    def make_movable(self, type_object, index_object, number_object, x1, y1, x2, y2):
        self.rectangle = self.canvas.create_rectangle(float(x1) - 5, float(y1) - 5, float(x2) + 5, float(y2) + 5,
                                                      outline='green')
        self.matrix_p_objects[type_object][index_object][number_object].make_movable(self.count_zoom, self.rectangle)
        self.matrix_p_objects[type_object][index_object][number_object].make_movable(self.count_zoom, self.rectangle)
        self.matrix_p_objects[type_object][index_object][number_object].make_movable(self.count_zoom, self.rectangle)

    def delete_unplaced_object(self):
        self.canvas.unbind("<Button-1>")

    def add_object(self, button_type, button_index):
        self.type_object = button_type
        self.index_object = button_index
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        if not self.list_erased_positions_p_objects[self.type_object][self.index_object]:
            self.index_matrix_p_objects[self.type_object][self.index_object] = \
                self.index_matrix_p_objects[self.type_object][self.index_object] + 1
            new_object = Pneumatics_Objects_File.PneumaticsObject(event, self.canvas,
                                                                  self.photos_list[self.type_object][self.index_object],
                                                                  self.type_object,
                                                                  self.index_object,
                                                                  self.index_matrix_p_objects[self.type_object][
                                                                      self.index_object],
                                                                  self.count_zoom,
                                                                  self.rectangle_canvas)
            self.matrix_p_objects[self.type_object][self.index_object].append(new_object)
        else:
            new_object = Pneumatics_Objects_File.PneumaticsObject(event, self.canvas,
                                                                  self.photos_list[self.type_object][self.index_object],
                                                                  self.type_object,
                                                                  self.index_object,
                                                                  self.list_erased_positions_p_objects[
                                                                      self.type_object][self.index_object]
                                                                  [len(self.list_erased_positions_p_objects[
                                                                           self.type_object][self.index_object]) - 1],
                                                                  self.count_zoom,
                                                                  self.rectangle_canvas)
            self.matrix_p_objects[self.type_object][self.index_object][
                self.list_erased_positions_p_objects[self.type_object][self.index_object][
                    len(self.list_erased_positions_p_objects[self.type_object][self.index_object]) - 1]] = new_object
            del self.list_erased_positions_p_objects[self.type_object][self.index_object][
                len(self.list_erased_positions_p_objects[self.type_object][self.index_object]) - 1]
        self.canvas.unbind("<Button-1>")
        self.release_button()

    def add_functions_for_buttons(self, release_button_function):
        # call in main function, add functions from addable buttons
        self.release_button = release_button_function

    def zoom_in(self):
        if self.count_zoom < 1:
            self.count_zoom = self.count_zoom + 1
            self.canvas.scale("all", 0, 0, 2, 2)
        for i in range(0, 3):
            for j in range(0, len(self.matrix_p_objects[i])):
                for k in range(0, len(self.matrix_p_objects[i][j])):
                    if None != self.matrix_p_objects[i][j][k]:
                        self.matrix_p_objects[i][j][k].zoom_image(self.count_zoom)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom_out(self):
        if self.count_zoom > -2:
            self.count_zoom = self.count_zoom - 1
            self.canvas.scale("all", 0, 0, 0.5, 0.5)
        for i in range(0, 3):
            for j in range(0, len(self.matrix_p_objects[i])):
                for k in range(0, len(self.matrix_p_objects[i][j])):
                    if None != self.matrix_p_objects[i][j][k]:
                        self.matrix_p_objects[i][j][k].zoom_image(self.count_zoom)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_resize(self, event):
        if self.frame_workspace.winfo_exists():
            self.zoom_buttons.place(y=self.root.winfo_height() - 50)
