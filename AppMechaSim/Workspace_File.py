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
        self.connections_button = tk.Button(self.zoom_buttons, text="Connections", command=self.connections)
        self.connections_button.pack(side=tk.LEFT)
        self.background_default_color = self.connections_button['bg']
        self.flag_connections = 0

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

        # connections
        self.connections_list = []
        # each element contain a list with two elements (element =[type, number, index, connection number])
        self.lines_for_connections_list = [[]]
        # each element contain a list with every line drowned for a connection
        self.store_digits = None
        self.first_connection = 0
        self.second_connection = 0
        self.first_point_connection_x = 0
        self.first_point_connection_y = 0
        self.second_point_connection_x = 0
        self.second_point_connection_y = 0
        self.flag_first_line = 0
        self.flag_last_line = 0
        self.line_coords = None
        self.next_line_coords = None
        self.previous_line_coords = None
        self.temp_line = None
        self.new_line_coords = None
        self.index_connections = -1
        self.my_menubar = MenuBar_File.MenuBar(self.root, self.update_rectangle_canvas, self.update_sim_buttons_state)

    def connections(self):
        self.flag_connections = 1 - self.flag_connections
        if self.flag_connections == 1:
            self.connections_button.configure(bg='green')
            for i in range(0, 3):
                for j in range(0, len(self.matrix_p_objects[i])):
                    for k in range(0, len(self.matrix_p_objects[i][j])):
                        if self.matrix_p_objects[i][j][k] is not None:
                            self.matrix_p_objects[i][j][k].show_connections(1)
                            if hasattr(self.matrix_p_objects[i][j][k], 'tag_connection'):
                                for l in range(0, len(self.matrix_p_objects[i][j][k].tag_connection)):
                                    self.canvas.tag_bind(str(self.matrix_p_objects[i][j][k].tag_connection[l]),
                                                         "<Enter>",
                                                         lambda event: self.check_hand_enter())
                                    self.canvas.tag_bind(str(self.matrix_p_objects[i][j][k].tag_connection[l]),
                                                         "<Button-1>",
                                                         lambda event: self.connect_function())
                                    self.canvas.tag_bind(str(self.matrix_p_objects[i][j][k].tag_connection[l]),
                                                         "<Leave>",
                                                         lambda event: self.check_hand_leave())
        else:
            self.connections_button.configure(bg=self.background_default_color)
            for i in range(0, 3):
                for j in range(0, len(self.matrix_p_objects[i])):
                    for k in range(0, len(self.matrix_p_objects[i][j])):
                        if self.matrix_p_objects[i][j][k] is not None:
                            self.matrix_p_objects[i][j][k].show_connections(0)
                            if hasattr(self.matrix_p_objects[i][j][k], 'tag_connection'):
                                for l in range(0, len(self.matrix_p_objects[i][j][k].tag_connection)):
                                    self.canvas.tag_unbind(str(self.matrix_p_objects[i][j][k].tag_connection[l]),
                                                           "<Enter>")
                                    self.canvas.tag_unbind(str(self.matrix_p_objects[i][j][k].tag_connection[l]),
                                                           "<Button-1>")
                                    self.canvas.tag_unbind(str(self.matrix_p_objects[i][j][k].tag_connection[l]),
                                                           "<Leave>")

    def connect_function(self):
        item_id = self.canvas.find_withtag("current")[0]
        tags = self.canvas.gettags(item_id)
        x1, y1, x2, y2 = self.canvas.bbox(item_id)
        digits = [int(c) for c in tags[0] if c.isdigit()]
        # 0 is active
        # 1 is element
        # 2 is index element
        # 3 is index connection
        if self.first_connection == 0 and self.second_connection == 0:
            self.store_digits = digits
            self.first_connection = 1
            self.first_point_connection_x = int((x1 + x2) / 2)
            self.first_point_connection_y = int((y1 + y2) / 2)
        if self.first_connection == 1 and self.second_connection == 1:
            self.first_connection = 0
            self.second_connection = 0
            if self.store_digits != digits:
                self.second_point_connection_x = int((x1 + x2) / 2)
                self.second_point_connection_y = int((y1 + y2) / 2)
                self.connections_list.append([self.store_digits, digits])
                self.index_connections = self.index_connections + 1
                self.lines_for_connections_list.append([])
                temp = self.canvas.create_line(self.first_point_connection_x, self.first_point_connection_y,
                                               self.first_point_connection_x, self.second_point_connection_y,
                                               fill='black',
                                               width=2, tags=('scale', 'line'))
                self.lines_for_connections_list[self.index_connections].append(temp)
                temp = self.canvas.create_line(self.first_point_connection_x, self.second_point_connection_y,
                                               self.second_point_connection_x, self.second_point_connection_y,
                                               fill='black',
                                               width=2, tags=('scale', 'line'))
                self.lines_for_connections_list[self.index_connections].append(temp)
                self.canvas.tag_bind('line', "<Enter>", lambda event: self.mouse_enter_line())
                self.canvas.tag_bind('line', "<Leave>", lambda event: self.mouse_leave_line())

                self.canvas.tag_bind(str(self.matrix_p_objects[self.store_digits[0]][self.store_digits[1]][self.store_digits[2]].tag_connection[self.store_digits[3]]), "<Double-Button-1>",
                                     lambda event: self.double_click_erase())
                self.canvas.tag_unbind(str(self.matrix_p_objects[self.store_digits[0]][self.store_digits[1]][self.store_digits[2]].tag_connection[self.store_digits[3]]),
                                     "<Button-1>")
                self.canvas.tag_bind(str(self.matrix_p_objects[digits[0]][digits[1]][
                                             digits[2]].tag_connection[digits[3]]),
                                     "<Double-Button-1>",
                                     lambda event: self.double_click_erase())
                self.canvas.tag_unbind(str(self.matrix_p_objects[digits[0]][digits[1]][
                                               digits[2]].tag_connection[digits[3]]),
                                       "<Button-1>")

                for i in range(0, len(self.lines_for_connections_list[self.index_connections])):
                    self.canvas.tag_bind(self.lines_for_connections_list[self.index_connections][i],
                                         '<ButtonRelease-1>',
                                         lambda event, index=self.index_connections: self.stop_move_line(event, index))
                    self.canvas.tag_bind(self.lines_for_connections_list[self.index_connections][i], '<ButtonPress-1>',
                                         lambda event, index=self.index_connections: self.start_move_line(event, index))
                    self.canvas.tag_bind(self.lines_for_connections_list[self.index_connections][i], '<B1-Motion>',
                                         lambda event, index=self.index_connections: self.do_move_line(event, index))
                self.matrix_p_objects[self.store_digits[0]][self.store_digits[1]][self.store_digits[2]].make_green(
                    self.store_digits[3])
                self.matrix_p_objects[digits[0]][digits[1]][digits[2]].make_green(digits[3])
        if self.first_connection == 1 and self.second_connection == 0:
            self.second_connection = 1

    def double_click_erase(self):
        print("erase")

    def do_move_line(self, event, index):
        item_id = self.canvas.find_withtag("current")[0]
        new_line_coords = self.canvas.coords(item_id)
        if (new_line_coords[0] > new_line_coords[2] - 5) and (new_line_coords[0] < new_line_coords[2] + 5):
            # vertical
            dx = int(event.x - new_line_coords[0])
            self.canvas.move(item_id, dx, 0)
            if self.flag_first_line == 1:
                self.canvas.delete(self.lines_for_connections_list[index][1])
                self.lines_for_connections_list[index][1] = self.canvas.create_line(new_line_coords[2],
                                                                                    new_line_coords[3],
                                                                                    self.next_line_coords[2],
                                                                                    self.next_line_coords[3],
                                                                                    fill='black',
                                                                                    width=2, tags=('scale', 'line'))
                self.canvas.delete(self.temp_line)
                self.temp_line = self.canvas.create_line(self.line_coords[0], self.line_coords[1],
                                                         new_line_coords[0], new_line_coords[1], fill='black',
                                                         width=2, tags=('scale', 'line'))
            elif self.flag_last_line == 1:
                self.canvas.delete(self.temp_line)
                self.temp_line = self.canvas.create_line(new_line_coords[2], new_line_coords[3],
                                                         self.line_coords[2], self.line_coords[3], fill='black',
                                                         width=2, tags=('scale', 'line'))
                self.canvas.delete(
                    self.lines_for_connections_list[index][len(self.lines_for_connections_list[index]) - 2])
                self.lines_for_connections_list[index][
                    len(self.lines_for_connections_list[index]) - 2] = self.canvas.create_line(
                    self.previous_line_coords[0],
                    self.previous_line_coords[1],
                    new_line_coords[0],
                    new_line_coords[1],
                    fill='black',
                    width=2,
                    tags=('scale', 'line'))
            else:
                self.canvas.delete(self.lines_for_connections_list[index][self.current_line - 1])
                self.lines_for_connections_list[index][self.current_line - 1] = self.canvas.create_line(
                    self.previous_line_coords[0],
                    self.previous_line_coords[1],
                    new_line_coords[0],
                    new_line_coords[1],
                    fill='black',
                    width=2, tags=('scale', 'line'))
                self.canvas.delete(self.lines_for_connections_list[index][self.current_line + 1])
                self.lines_for_connections_list[index][self.current_line + 1] = self.canvas.create_line(
                    new_line_coords[2],
                    new_line_coords[3],
                    self.next_line_coords[
                        2],
                    self.next_line_coords[
                        3],
                    fill='black',
                    width=2, tags=(
                        'scale', 'line'))
        else:
            # horizontal
            last_position = new_line_coords[1]
            y = event.y - last_position
            self.canvas.move(item_id, 0, y)
            if self.flag_first_line == 1:
                self.canvas.delete(self.lines_for_connections_list[index][1])
                self.lines_for_connections_list[index][1] = self.canvas.create_line(new_line_coords[2],
                                                                                    new_line_coords[3],
                                                                                    self.next_line_coords[2],
                                                                                    self.next_line_coords[3],
                                                                                    fill='black',
                                                                                    width=2, tags=('scale', 'line'))
                self.canvas.delete(self.temp_line)
                self.temp_line = self.canvas.create_line(self.line_coords[0], self.line_coords[1],
                                                         new_line_coords[0], new_line_coords[1], fill='black',
                                                         width=2, tags=('scale', 'line'))
            elif self.flag_last_line == 1:
                self.canvas.delete(
                    self.lines_for_connections_list[index][len(self.lines_for_connections_list[index]) - 2])
                self.lines_for_connections_list[index][
                    len(self.lines_for_connections_list[index]) - 2] = self.canvas.create_line(
                    self.previous_line_coords[0],
                    self.previous_line_coords[1],
                    new_line_coords[0],
                    new_line_coords[1],
                    fill='black',
                    width=2,
                    tags=('scale', 'line'))
                self.canvas.delete(self.temp_line)
                self.temp_line = self.canvas.create_line(new_line_coords[2], new_line_coords[3],
                                                         self.line_coords[2], self.line_coords[3], fill='black',
                                                         width=2, tags=('scale', 'line'))
            else:
                self.canvas.delete(self.lines_for_connections_list[index][self.current_line - 1])
                self.lines_for_connections_list[index][self.current_line - 1] = self.canvas.create_line(
                    self.previous_line_coords[0],
                    self.previous_line_coords[1],
                    new_line_coords[0],
                    new_line_coords[1],
                    fill='black',
                    width=2, tags=('scale', 'line'))
                self.canvas.delete(self.lines_for_connections_list[index][self.current_line + 1])
                self.lines_for_connections_list[index][self.current_line + 1] = self.canvas.create_line(
                    new_line_coords[2],
                    new_line_coords[3],
                    self.next_line_coords[
                        2],
                    self.next_line_coords[
                        3],
                    fill='black',
                    width=2, tags=(
                        'scale', 'line'))

    def stop_move_line(self, event, index):
        if self.flag_first_line == 1:
            self.lines_for_connections_list[index].insert(0, self.temp_line)
            self.canvas.tag_bind(self.lines_for_connections_list[index][0], '<ButtonRelease-1>',
                                 lambda event, index2=index: self.stop_move_line(event, index2))
            self.canvas.tag_bind(self.lines_for_connections_list[index][0], '<ButtonPress-1>',
                                 lambda event, index2=index: self.start_move_line(event, index2))
            self.canvas.tag_bind(self.lines_for_connections_list[index][0], '<B1-Motion>',
                                 lambda event, index2=index: self.do_move_line(event, index2))
            self.canvas.tag_bind(self.lines_for_connections_list[index][2], '<ButtonRelease-1>',
                                 lambda event, index2=index: self.stop_move_line(event, index2))
            self.canvas.tag_bind(self.lines_for_connections_list[index][2], '<ButtonPress-1>',
                                 lambda event, index2=index: self.start_move_line(event, index2))
            self.canvas.tag_bind(self.lines_for_connections_list[index][2], '<B1-Motion>',
                                 lambda event, index2=index: self.do_move_line(event, index2))
        elif self.flag_last_line == 1:
            self.lines_for_connections_list[index].append(self.temp_line)
            self.canvas.tag_bind(
                self.lines_for_connections_list[index][len(self.lines_for_connections_list[index]) - 1],
                '<ButtonRelease-1>',
                lambda event, index2=index: self.stop_move_line(event, index2))
            self.canvas.tag_bind(
                self.lines_for_connections_list[index][len(self.lines_for_connections_list[index]) - 1],
                '<ButtonPress-1>',
                lambda event, index2=index: self.start_move_line(event, index2))
            self.canvas.tag_bind(
                self.lines_for_connections_list[index][len(self.lines_for_connections_list[index]) - 1],
                '<B1-Motion>',
                lambda event, index2=index: self.do_move_line(event, index2))
            self.canvas.tag_bind(
                self.lines_for_connections_list[index][len(self.lines_for_connections_list[index]) - 3],
                '<ButtonRelease-1>',
                lambda event, index2=index: self.stop_move_line(event, index2))
            self.canvas.tag_bind(
                self.lines_for_connections_list[index][len(self.lines_for_connections_list[index]) - 3],
                '<ButtonPress-1>',
                lambda event, index2=index: self.start_move_line(event, index2))
            self.canvas.tag_bind(
                self.lines_for_connections_list[index][len(self.lines_for_connections_list[index]) - 3],
                '<B1-Motion>',
                lambda event, index2=index: self.do_move_line(event, index2))
        else:
            self.canvas.tag_bind(self.lines_for_connections_list[index][self.current_line - 1],
                                 '<ButtonRelease-1>',
                                 lambda event, index2=index: self.stop_move_line(event, index2))
            self.canvas.tag_bind(self.lines_for_connections_list[index][self.current_line - 1],
                                 '<ButtonPress-1>',
                                 lambda event, index2=index: self.start_move_line(event, index2))
            self.canvas.tag_bind(self.lines_for_connections_list[index][self.current_line - 1],
                                 '<B1-Motion>',
                                 lambda event, index2=index: self.do_move_line(event, index2))
            self.canvas.tag_bind(self.lines_for_connections_list[index][self.current_line + 1],
                                 '<ButtonRelease-1>',
                                 lambda event, index2=index: self.stop_move_line(event, index2))
            self.canvas.tag_bind(self.lines_for_connections_list[index][self.current_line + 1],
                                 '<ButtonPress-1>',
                                 lambda event, index2=index: self.start_move_line(event, index2))
            self.canvas.tag_bind(self.lines_for_connections_list[index][self.current_line + 1],
                                 '<B1-Motion>',
                                 lambda event, index2=index: self.do_move_line(event, index2))
        self.flag_first_line = 0
        self.flag_last_line = 0
        self.temp_line = None

    def start_move_line(self, event, index):
        item_id = self.canvas.find_withtag("current")[0]
        new_line_coords = self.canvas.coords(item_id)
        self.line_coords = new_line_coords
        for i in range(0, len(self.lines_for_connections_list[index])):
            if self.lines_for_connections_list[index][i] == item_id:
                if i == 0:
                    self.flag_first_line = 1
                    self.next_line_coords = self.canvas.coords(self.lines_for_connections_list[index][1])
                elif i == (len(self.lines_for_connections_list[index]) - 1):
                    self.flag_last_line = 1
                    self.previous_line_coords = self.canvas.coords(
                        self.lines_for_connections_list[index][len(self.lines_for_connections_list[index]) - 2])
                else:
                    self.previous_line_coords = self.canvas.coords(self.lines_for_connections_list[index][i - 1])
                    self.next_line_coords = self.canvas.coords(self.lines_for_connections_list[index][i + 1])
                    self.current_line = i

    def mouse_enter_line(self):
        item_id = self.canvas.find_withtag("current")[0]
        new_line_coords = self.canvas.coords(item_id)
        if (new_line_coords[0] > new_line_coords[2] - 5) and (new_line_coords[0] < new_line_coords[2] + 5):
            self.canvas.config(cursor="sb_h_double_arrow")
        else:
            self.canvas.config(cursor="sb_v_double_arrow")

    def mouse_leave_line(self):
        self.canvas.config(cursor="")

    def check_hand_enter(self):
        self.canvas.config(cursor="hand2")

    def check_hand_leave(self, ):
        self.canvas.config(cursor="")

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
            if self.flag_connections == 1:
                for i in range(0, 3):
                    for j in range(0, len(self.matrix_p_objects[i])):
                        for k in range(0, len(self.matrix_p_objects[i][j])):
                            if self.matrix_p_objects[i][j][k] is not None:
                                self.matrix_p_objects[i][j][k].show_connections(0)
                                self.matrix_p_objects[i][j][k].show_connections(1)
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

    def update_connection_points(self, type, index, number, new_x, new_y):
        type = int(type)
        index = int(index)
        number = int(number)
        for i in range(0, len(self.connections_list)):
            if self.connections_list[i][0][0] == type and self.connections_list[i][0][1] == index and \
                    self.connections_list[i][0][2] == number:
                new_x, new_y = self.canvas.coords(
                    self.matrix_p_objects[type][index][number].connection_id_image[self.connections_list[i][0][3]])
                x1, y1, x2, y2 = self.canvas.coords(
                    self.lines_for_connections_list[i][1])
                if (x1 + 5) > x2 > (x1 - 5): # vertical
                    self.canvas.delete(self.lines_for_connections_list[i][1])
                    self.canvas.delete(self.lines_for_connections_list[i][0])
                    self.lines_for_connections_list[i][0] = self.canvas.create_line(
                        new_x, new_y,
                        x1, new_y,
                        fill='black',
                        width=2, tags=('scale', 'line'))
                    self.lines_for_connections_list[i][1] = self.canvas.create_line(
                        x1, new_y,
                        x2, y2,
                        fill='black',
                        width=2, tags=('scale', 'line'))
                else: # horizontal
                    self.canvas.delete(self.lines_for_connections_list[i][1])
                    self.canvas.delete(self.lines_for_connections_list[i][0])
                    self.lines_for_connections_list[i][1] = self.canvas.create_line(
                        new_x, new_y,
                        new_x, y1,
                        fill='black',
                        width=2, tags=('scale', 'line'))
                    self.lines_for_connections_list[i][0] = self.canvas.create_line(
                        new_x, y1,
                        x2, y2,
                        fill='black',
                        width=2, tags=('scale', 'line'))

                self.canvas.tag_bind(self.lines_for_connections_list[i][1], '<ButtonRelease-1>',
                                         lambda event, index=self.index_connections: self.stop_move_line(event, index))
                self.canvas.tag_bind(self.lines_for_connections_list[i][1], '<ButtonPress-1>',
                                         lambda event, index=self.index_connections: self.start_move_line(event, index))
                self.canvas.tag_bind(self.lines_for_connections_list[i][1], '<B1-Motion>',
                                         lambda event, index=self.index_connections: self.do_move_line(event, index))
                self.canvas.tag_bind(self.lines_for_connections_list[i][0], '<ButtonRelease-1>',
                                     lambda event, index=self.index_connections: self.stop_move_line(event, index))
                self.canvas.tag_bind(self.lines_for_connections_list[i][0], '<ButtonPress-1>',
                                     lambda event, index=self.index_connections: self.start_move_line(event, index))
                self.canvas.tag_bind(self.lines_for_connections_list[i][0], '<B1-Motion>',
                                     lambda event, index=self.index_connections: self.do_move_line(event, index))
            if self.connections_list[i][1][0] == type and self.connections_list[i][1][1] == index and \
                    self.connections_list[i][1][2] == number:
                new_x, new_y = self.canvas.coords(
                    self.matrix_p_objects[type][index][number].connection_id_image[self.connections_list[i][1][3]])
                x1, y1, x2, y2 = self.canvas.coords(
                    self.lines_for_connections_list[i][len(self.lines_for_connections_list[i]) - 2])
                if (x1 + 5) > x2 > (x1 - 5):
                    self.canvas.delete(self.lines_for_connections_list[i][len(self.lines_for_connections_list[i]) - 2])
                    self.canvas.delete(self.lines_for_connections_list[i][len(self.lines_for_connections_list[i]) - 1])
                    self.lines_for_connections_list[i][
                        len(self.lines_for_connections_list[i]) - 2] = self.canvas.create_line(
                        x1, y1,
                        x2, new_y,
                        fill='black',
                        width=2, tags=('scale', 'line'))
                    self.lines_for_connections_list[i][
                        len(self.lines_for_connections_list[i]) - 1] = self.canvas.create_line(
                        x1, new_y,
                        new_x, new_y,
                        fill='black',
                        width=2, tags=('scale', 'line'))
                else:
                    self.canvas.delete(self.lines_for_connections_list[i][len(self.lines_for_connections_list[i]) - 2])
                    self.canvas.delete(self.lines_for_connections_list[i][len(self.lines_for_connections_list[i]) - 1])
                    self.lines_for_connections_list[i][
                        len(self.lines_for_connections_list[i]) - 2] = self.canvas.create_line(
                        x1, y1,
                        new_x, y2,
                        fill='black',
                        width=2, tags=('scale', 'line'))
                    self.lines_for_connections_list[i][
                        len(self.lines_for_connections_list[i]) - 1] = self.canvas.create_line(
                        new_x, y1,
                        new_x, new_y,
                        fill='black',
                        width=2, tags=('scale', 'line'))

                self.canvas.tag_bind(self.lines_for_connections_list[i][
                                             len(self.lines_for_connections_list[i]) - 1], '<ButtonRelease-1>',
                                         lambda event, index=self.index_connections: self.stop_move_line(event, index))
                self.canvas.tag_bind(self.lines_for_connections_list[i][
                                             len(self.lines_for_connections_list[i]) - 1], '<ButtonPress-1>',
                                         lambda event, index=self.index_connections: self.start_move_line(event, index))
                self.canvas.tag_bind(self.lines_for_connections_list[i][
                                             len(self.lines_for_connections_list[i]) - 1], '<B1-Motion>',
                                         lambda event, index=self.index_connections: self.do_move_line(event, index))
                self.canvas.tag_bind(self.lines_for_connections_list[i][
                                         len(self.lines_for_connections_list[i]) - 2], '<ButtonRelease-1>',
                                     lambda event, index=self.index_connections: self.stop_move_line(event, index))
                self.canvas.tag_bind(self.lines_for_connections_list[i][
                                         len(self.lines_for_connections_list[i]) - 2], '<ButtonPress-1>',
                                     lambda event, index=self.index_connections: self.start_move_line(event, index))
                self.canvas.tag_bind(self.lines_for_connections_list[i][
                                         len(self.lines_for_connections_list[i]) - 2], '<B1-Motion>',
                                     lambda event, index=self.index_connections: self.do_move_line(event, index))

    def send_data_from_parameters(self, new_tk_photo, flag_left_control, flag_right_control):
        self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
            self.current_photo_number].flag_left_control = flag_left_control
        self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
            self.current_photo_number].flag_right_control = flag_right_control
        if flag_left_control[0] == 1 and flag_right_control[0] == 0:
            self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
                self.current_photo_number].adding_from_controls = int(
                self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
                    self.current_photo_number].last_size_controls / 2)
        if flag_left_control[0] == 0 and flag_right_control[0] == 1:
            self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
                self.current_photo_number].adding_from_controls = - int(
                self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
                    self.current_photo_number].last_size_controls / 2)
        if flag_left_control[0] == flag_right_control[0]:
            self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
                self.current_photo_number].adding_from_controls = 0
        if self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
            self.current_photo_number].flag_connections == 1:
            self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
                self.current_photo_number].show_connections(0)
            self.matrix_p_objects[self.current_photo_type][self.current_photo_index][
                self.current_photo_number].show_connections(1)
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
        self.matrix_p_objects[type_object][index_object][number_object].make_movable(self.count_zoom, self.rectangle,
                                                                                     self.update_connection_points)

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
                    if self.matrix_p_objects[i][j][k] is not None:
                        self.matrix_p_objects[i][j][k].zoom_image(self.count_zoom)
        self.flag_connections = 0
        self.connections()
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
        self.flag_connections = 0
        self.connections()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_resize(self, event):
        if self.frame_workspace.winfo_exists():
            self.zoom_buttons.place(y=self.root.winfo_height() - 50)
