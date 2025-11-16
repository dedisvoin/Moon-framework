import sys
sys.path.append('./')

from Moon.python.Vectors import *
from Moon.python.Window import *
from Moon.python.Rendering.Shapes import *
from Moon.python import Threader
from Moon.python.Inputs import *

circle_shape = CircleShape(5)
circle_shape.set_position(Vector2f(300, 300))
circle_shape.set_origin_radius(70)
circle_shape.set_color(COLOR_ORANGE)

def AppOne(worker: Threader.Worker):
    win_1 = Window(700, 700, "AppOne")
    window_events = WindowEvents()
    print(win_1.get_header_color())

    while win_1.update(window_events):
        win_1.clear()
        circle_shape.set_position(win_1.get_center(False))
        win_1.draw(circle_shape)
        circle_shape.set_angle(win_1.get_global_timer(180))
        if MouseInterface.get_click('left') and win_1.has_focus():
            circle_shape.set_color(Color.random())
        win_1.display()
    win_1.close()

def AppTwo(worker: Threader.Worker):
    win_2 = Window(500, 500, "AppTwo")
    window_events = WindowEvents()
    print(win_2.get_header_color())

    while win_2.update(window_events):
        win_2.clear()
        circle_shape.set_position(win_2.get_center(False))
        win_2.draw(circle_shape)
        win_2.display()
    win_2.close()

worker_1 = Threader.Worker()
worker_2 = Threader.Worker()

worker_1.start(AppOne)
worker_2.start(AppTwo)
