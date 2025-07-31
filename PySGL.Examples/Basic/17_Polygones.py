import sys
sys.path.append("./")
from PySGL.python.Window import *
from PySGL.python.Rendering.Shapes import *
from PySGL.python.Inputs import MouseInterface

window = Window(title="test").set_view_info()
window.set_wait_fps(FPS_UNLIMIT_CONST)

events = WindowEvents()



poly = PolygoneShape([], COLOR_RED)

while window.is_open():
    if not window.update(events): window.close()
    window.clear()

    if MouseInterface.get_click('left'):
        poly.append_point_to_end(MouseInterface.get_position_in_window(window))

    if MouseInterface.get_click('right'):
        poly.append_point_to_begin(MouseInterface.get_position_in_window(window))


    window.draw(poly)
    window.view_info()
    window.display()
    
