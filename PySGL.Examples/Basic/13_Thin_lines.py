import sys
sys.path.append("./")
from PySGL.python.Window import *
from PySGL.python.Colors import *
from PySGL.python.Rendering.Shapes import *
from PySGL.python.Inputs import MouseInterface

window = Window().set_view_info()
window.set_wait_fps(60)
events = WindowEvents()


line = LinesThinShape()


while window.update(events):
    window.clear()
    
    if MouseInterface.get_click('left'):
        line.append_point_to_end(MouseInterface.get_position_in_window(window), random_color_with_alpha(255))
    if MouseInterface.get_click('right'):
        line.append_point_to_begin(MouseInterface.get_position_in_window(window), random_color_with_alpha(255))
    if MouseInterface.get_click('middle'):
        line.clear()

    

    window.draw(line)

    window.view_info()
    window.display()

