import sys
import random
sys.path.append("./")
from PySGL.python.Window import *

from PySGL.python.Audio import *
from PySGL.python.Rendering.Text import *
from PySGL.python.Inputs import MouseInterface


window = Window(style=Window.Style.No).set_view_info()
events = WindowEvents()
window.set_wait_fps(60)
window.set_ghosting().set_ghosting_min_alpha(70)
while window.update(events):

    window.clear()
    mouse_speed = MouseInterface.get_speed()
    if MouseInterface.get_press("left"):
        window_pos = window.get_position().to_float()
        window.set_position(*(window_pos + mouse_speed.to_float()).to_int().xy)


    


    window.view_info()
    window.display()