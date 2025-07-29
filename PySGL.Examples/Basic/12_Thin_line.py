import sys
sys.path.append("./")
from PySGL.python.Window import *
from PySGL.python.Colors import *
from PySGL.python.Rendering.Shapes import *


window = Window().set_view_info()
window.set_wait_fps(60)
events = WindowEvents()


line = LineThinShape()

line.set_points(300, 300, 600, 450)
line.set_color(COLOR_YELLOW)
line.set_start_color(COLOR_GREEN)


while window.update(events):
    window.clear()
    
    window.draw(line)

    window.view_info()
    window.display()

