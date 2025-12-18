import sys
sys.path.append('./')
from Moon.python.Vectors import *
from Moon.python.Window import *
from Moon.python.Rendering.Shapes import *
from Moon.python.Threader import *
from Moon.python.System import *


window = Window(1000, 1000, style=Window.Style.Default, dynamic_update=True)
window.set_view_info()
window.set_wait_fps(FPS_UNLIMIT_CONST)

events = WindowEvents()

polygone = PolygonShape()
polygone.add_vertex(Vector2f(200, 200))
polygone.add_vertex(Vector2f(800, 200))
polygone.add_vertex(Vector2f(500, 800))
polygone.set_all_vertices_colors([COLOR_RED, COLOR_GREEN, COLOR_BLUE])




while window.update(events):

    window.clear()
    window.draw(polygone)
    win_size = window.get_size(True).as_list()
    polygone.get_vertex(0).position = Vector2f(win_size[0] / 10, win_size[1] / 10)
    polygone.get_vertex(1).position = Vector2f(win_size[0] / 10 * 9, win_size[1] / 10)
    polygone.get_vertex(2).position = Vector2f(win_size[0] / 2, win_size[1] / 10 * 9)
    
    window.view_info()
    window.display()


window.close()

