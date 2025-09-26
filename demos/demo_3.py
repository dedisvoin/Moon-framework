import sys
sys.path.append('./')

from Moon.python.Window import *

from Moon.python.Vectors import Vector2f
from Moon.python.Rendering.Shapes import CircleShape


window = Window( title="Moon Framework Demo", style=Window.Style.FullScreenDesktop)
window.set_wait_fps(60)

window.set_view_info()

window_events = WindowEvents()



pos = window.get_center(True)
speed = Vector2f.random() * 100

circle = CircleShape()
circle.set_origin_radius(50)
circle.set_color(COLOR_RED)



while window.update(window_events):
    window.clear()

    pos += speed * window.get_render_time(10)
    if pos.x < 50 or pos.x > window.get_size().x - 50:
        speed.x *= -1
        pos.x = max(50, min(pos.x, window.get_size().x - 50))
    if pos.y < 50 or pos.y > window.get_size().y - 50:
        speed.y *= -1
        pos.y = max(50, min(pos.y, window.get_size().y - 50))

    circle.set_position(*pos.xy)
    window.draw(circle)

    window.view_info()
    window.display()
