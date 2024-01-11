import PIL
from PIL import Image, ImageTk
import tkinter as tk
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


spring_left = Image.open(resource_path('images/control_spring.png'))
spring_right = spring_left.transpose(Image.FLIP_LEFT_RIGHT)
mechanical_left = Image.open(resource_path('images/control_mechanic.png'))
mechanical_right = mechanical_left.transpose(Image.FLIP_LEFT_RIGHT)
manual_left = Image.open(resource_path('images/control_manual.png'))
manual_right = manual_left.transpose(Image.FLIP_LEFT_RIGHT)
pneumatic_left = Image.open(resource_path('images/control_pneumatic.png'))
pneumatic_right = pneumatic_left.transpose(Image.FLIP_LEFT_RIGHT)
electric_left = Image.open(resource_path('images/control_electric.png'))
electric_right = electric_left.transpose(Image.FLIP_LEFT_RIGHT)
list_controls = [[None] * 12, [None] * 12, [None] * 12]
list_controls[0] = [None, spring_left, mechanical_left, manual_left, pneumatic_left, electric_left,
                    None, spring_right, mechanical_right, manual_right, pneumatic_right, electric_right]
list_controls[1] = list_controls[0]

empty_big_image = Image.new("RGBA", (50, 100), (0, 0, 0, 0))
empty_big_image.paste(spring_left, (0, 0))
spring_empty_left = empty_big_image
spring_empty_right = spring_empty_left.transpose(Image.FLIP_LEFT_RIGHT)

empty_big_image = Image.new("RGBA", (50, 100), (0, 0, 0, 0))
empty_big_image.paste(spring_left, (0, 0))
empty_big_image.paste(mechanical_left, (0, 50))
spring_mechanical_left = empty_big_image
spring_mechanical_right = spring_mechanical_left.transpose(Image.FLIP_LEFT_RIGHT)

empty_big_image = Image.new("RGBA", (50, 100), (0, 0, 0, 0))
empty_big_image.paste(spring_left, (0, 0))
empty_big_image.paste(manual_left, (0, 50))
spring_manual_left = empty_big_image
spring_manual_right = spring_manual_left.transpose(Image.FLIP_LEFT_RIGHT)

empty_big_image = Image.new("RGBA", (50, 100), (0, 0, 0, 0))
empty_big_image.paste(spring_left, (0, 0))
empty_big_image.paste(pneumatic_left, (0, 50))
spring_pneumatic_left = empty_big_image
spring_pneumatic_right = spring_pneumatic_left.transpose(Image.FLIP_LEFT_RIGHT)

empty_big_image = Image.new("RGBA", (50, 100), (0, 0, 0, 0))
empty_big_image.paste(spring_left, (0, 0))
empty_big_image.paste(electric_left, (0, 50))
spring_electric_left = empty_big_image
spring_electric_right = spring_electric_left.transpose(Image.FLIP_LEFT_RIGHT)

list_controls[2] = [None, spring_empty_left, spring_mechanical_left, spring_manual_left, spring_pneumatic_left,
                    spring_electric_left,
                    None, spring_empty_right, spring_mechanical_right, spring_manual_right, spring_pneumatic_right,
                    spring_electric_right]

p_a_nr_elements = 8
p_a_photos = [None] * p_a_nr_elements
p_a_photos[1] = Image.open(resource_path('images/cylinder_single_acting.png'))
p_a_photos[2] = Image.open(resource_path('images/cylinder_double_acting_1.png'))
p_a_photos[3] = Image.open(resource_path('images/cylinder_double_acting_2.png'))
p_a_photos[4] = Image.open(resource_path('images/valve_2_2.png'))
p_a_photos[5] = Image.open(resource_path('images/valve_3_2.png'))
p_a_photos[6] = Image.open(resource_path('images/valve_5_3.png'))
p_a_photos[7] = Image.open(resource_path('images/compressor.png'))
p_a_buttons = [None] * p_a_nr_elements
p_a_buttons[1] = Image.open(resource_path('images/buttons/cylinder_single_acting_button.png'))
p_a_buttons[2] = Image.open(resource_path('images/buttons/cylinder_double_acting_1_button.png'))
p_a_buttons[3] = Image.open(resource_path('images/buttons/cylinder_double_acting_2_button.png'))
p_a_buttons[4] = Image.open(resource_path('images/buttons/valve_2_2_button.png'))
p_a_buttons[5] = Image.open(resource_path('images/buttons/valve_3_2_button.png'))
p_a_buttons[6] = Image.open(resource_path('images/buttons/valve_5_3_button.png'))
p_a_buttons[7] = Image.open(resource_path('images/buttons/compressor_button.png'))

p_p_nr_elements = 3
p_p_photos = [None] * p_p_nr_elements
p_p_photos[1] = Image.open(resource_path('images/check_valve.png'))
p_p_photos[2] = Image.open(resource_path('images/muffler.png'))
p_p_buttons = [None] * p_a_nr_elements
p_p_buttons[1] = Image.open(resource_path('images/buttons/check_valve_button.png'))
p_p_buttons[2] = Image.open(resource_path('images/buttons/muffler_button.png'))

p_f_nr_elements = 2
p_f_photos = [None] * p_f_nr_elements
p_f_photos[1] = Image.open(resource_path('images/regulator.png'))
p_f_buttons = [None] * p_f_nr_elements
p_f_buttons[1] = Image.open(resource_path('images/buttons/regulator_button.png'))

start_button = Image.open(resource_path("images/sim_buttons/start_button.png"))
pause_button = Image.open(resource_path("images/sim_buttons/pause_button.png"))
continue_button = Image.open(resource_path("images/sim_buttons/continue_button.png"))
stop_button = Image.open(resource_path("images/sim_buttons/stop_button.png"))

simulation_buttons = [start_button, pause_button, continue_button, stop_button]
