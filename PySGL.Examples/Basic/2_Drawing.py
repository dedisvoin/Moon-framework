import sys
sys.path.append("./")
from PySGL.python.Window import *
from PySGL.python.Colors import *
from PySGL.python.Rendering.Shapes import *


window = Window().set_view_info()
window.set_wait_fps(FPS_UNLIMIT_CONST)
events = WindowEvents()
window.enable_ghosting()


rect = RectangleShape(200, 200).set_origin(100, 100).set_color(COLOR_RED)
rect.set_position(Vector2f(300,300))
rect.set_angle(60)
rect.set_scale(1)
rect.set_outline_thickness(10)
rect.set_outline_color(COLOR_BLACK)
rect2 = rect.copy().set_scale(0.5).set_outline_thickness(20)
rect2.set_position(Vector2f(500, 230))


circle = CircleShape(10).set_origin_radius(60).set_color(COLOR_GREEN).set_outline_thickness(10).set_outline_color(COLOR_BLACK)
circle.set_position(300, 200)


line = LineShape().set_start_point(100, 400).set_end_point(500, 300).set_color(COLOR_BLUE).set_width(10).set_outline_thickness(10).set_outline_color(COLOR_BLACK).set_rounded()

while window.update(events):
    rect.set_angle(rect.get_angle() + 100 * window.get_render_time())
    circle.set_angle(circle.get_angle() - 300 * window.get_render_time())
    window.clear()
    window.draw(rect)
    window.draw(rect2)
    window.draw(circle)
    window.draw(line)
    window.view_info()
    window.display()

