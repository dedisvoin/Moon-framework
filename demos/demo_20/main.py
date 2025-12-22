import sys
sys.path.append('./')
from Moon.python.Vectors import *
from Moon.python.Window import *
from Moon.python.Inputs import *


# Инициализируем окно
window = Window(1000, 1000, dynamic_update=True)
window.set_view_info()
window.set_wait_fps(FPS_VSYNC_CONST)
window.set_max_fps_history(30)
events = WindowEvents()


rect = RectangleShape()
rect.color = COLOR_EMERALD
rect.size = Vec2f(200, 200)
rect.outline_color = COLOR_BLACK
rect.origin = rect.size / 2


circle = CircleShape(5)
circle.position = Vec2f(300, 300)
circle.color = COLOR_RED
circle.origin = Vec2f(100, 100)
circle.radius = 100



while window.update(events):
    window.clear()
    rect.position = MouseInterface.get_position_in_window(window)
    rect.angle += 1
    rect.outline_thickness = abs(math.sin(window.get_global_timer() * 3)) * 10 + 10
    window.draw(rect)
    window.draw(circle)

    window.view_info()
    window.display()