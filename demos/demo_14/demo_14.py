import sys
sys.path.append('./')

from Moon.python.Inputs import *
from Moon.python.Window import *
from Moon.python.Rendering.Shapes import *

window = Window(title="Test")
window.set_wait_fps(FPS_VSYNC_CONST)
window.set_view_info()
window_events = WindowEvents()


ls = LineShape().init_points()
ls.set_start_point(Vec2f(200, 200))
ls.set_end_point(Vec2f(400, 400))
ls.set_color(COLOR_GREEN)
ls.get_end_point().position = Vec2f.zero()
ls.get_end_point().color = COLOR_ORANGE

while window.update(window_events):
    window.clear()

    window.draw(ls)
    #window.view_info()


    window.display()
