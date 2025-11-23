import sys
sys.path.append('./')
from Moon.python.Vectors import *
from Moon.python.Window import *
from Moon.python.Rendering.Shaders import *
from Moon.python.Rendering.Sprites import *
from Moon.python.Inputs import *
from Moon.python.System import *

# Инициализируем окно
window = Window(1000, 1000)
window.set_view_info()
window.set_wait_fps(180)
window.set_max_fps_history(30)
events = WindowEvents()


rect = RectangleShape()
rect.size = Vector2f(200, 200)
rect.color = COLOR_EMERALD
rect.origin = Vector2f(100, 100)
rect.outline_color = COLOR_BLACK


while window.update(events):
    window.clear()
    rect.position = MouseInterface.get_position_in_window(window)
    rect.angle += 1
    rect.outline_thickness = abs(math.sin(window.get_global_timer() * 3)) * 10 + 10
    rect.origin = Vector2f(
        200 * abs(math.sin(window.get_global_timer())),
        200 * abs(math.cos(window.get_global_timer()))
    )
    window.draw(rect)

    window.view_info()
    window.display()