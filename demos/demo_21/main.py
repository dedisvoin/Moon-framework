import sys
sys.path.append('./')
from Moon.python.Vectors import *
from Moon.python.Window import *
from Moon.python.Inputs import *


# Инициализируем окно
window = Window(1000, 1000)
window.set_view_info()
window.set_wait_fps(160)
window.set_max_fps_history(40)
events = WindowEvents()


rect = RectangleShape()
rect.color = COLOR_EMERALD
rect.size = Vector2f(200, 200)
rect.outline_color = COLOR_BLACK
rect.origin = rect.size / 2
rect.position.x = 10
rect.position = Vector2f(400, 400)
rect.color.r = 255
rect.color.g = 0
rect.color.b = 0
print(rect.color)

circle = CircleShape()
circle.color = COLOR_RED
circle.position = Vector2f(600, 200)
circle.radius = 100
circle.color = COLOR_BLACK
circle.color.g = 200
circle.color.b = 200
circle.color.r = 20


while window.update(events):
    window.clear()
    rect.angle += window.get_render_time() * 100
    window.draw(rect)

    window.draw(circle)

    window.view_info()
    window.display()
