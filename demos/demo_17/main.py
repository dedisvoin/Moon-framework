import sys
sys.path.append('./')

from Moon.python.Vectors import *
from Moon.python.Window import *
from Moon.python.Rendering.Shapes import *
from Moon.python import Threader
from Moon.python.Inputs import *

circle_shape = CircleShape(3)
circle_shape.set_position(Vector2f(300, 300))
circle_shape.set_origin_radius(120)
circle_shape.set_color(COLOR_ORANGE)

semaphore = Threader.Lock()

def AppOne(worker: Threader.Worker):
    win_1 = Window(700, 700, "AppOne")
    win_1.set_view_info()
    win_1.set_wait_fps(FPS_VSYNC_CONST)
    window_events = WindowEvents()


    while win_1.update(window_events):
        circle_shape.set_angle(win_1.get_global_timer(180))
        win_1.clear()
        with semaphore:
            circle_shape.set_position(win_1.get_center(False))
            win_1.draw(circle_shape)
            
        if MouseInterface.get_click('left') and win_1.has_focus():
            circle_shape.set_color(Color.random())
        
        win_1.view_info()
        win_1.display()
    win_1.close()

def AppTwo(worker: Threader.Worker):
    win_2 = Window(500, 500, "AppTwo")
    window_events = WindowEvents()
    win_2.set_view_info()

    while win_2.update(window_events):
        win_2.clear()
        with semaphore:
            circle_shape.set_position(win_2.get_center(False))
            win_2.draw(circle_shape)
            
        win_2.view_info()
        win_2.display()
        
    win_2.close()

worker_1 = Threader.Worker()
worker_2 = Threader.Worker()

worker_1.start(AppOne)
worker_2.start(AppTwo)
