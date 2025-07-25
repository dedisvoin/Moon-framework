import sys
sys.path.append("./")
from PySGL.python.Window import *
from PySGL.python.Colors import *
from PySGL.python.rendering.Shapes import *


window = Window().set_view_info()
events = WindowEvents()


rect = BaseRectangleShape(200, 200).set_origin(100, 100).set_color(COLOR_RED)
rect.set_position(400, 400)
rect.set_angle(60)

circle = BaseCircleShape(10).set_origin_radius(60).set_color(COLOR_GREEN).set_outline_thickness(2).set_outline_color(COLOR_RED)
circle.set_position(300, 200)


line = LineShape().set_start_pos(100, 400).set_end_pos(500, 300).set_color(COLOR_BLUE).set_width(30).set_outline_thickness(2).set_outline_color(COLOR_RED)

while window.update(events):
    rect.set_angle(rect.get_angle() + 100 * window.get_render_time())
    circle.set_angle(circle.get_angle() - 300 * window.get_render_time())
    window.clear()
    window.draw(rect)
    window.draw(circle)
    window.draw(line)
    window.view_info()
    window.display()
