import sys
sys.path.append("./")
from Moon.python.Window import *
from Moon.python.Colors import *
from Moon.python.Rendering.Shapes import *


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

