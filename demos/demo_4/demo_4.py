import sys
sys.path.append('./')


from Moon.python.Inputs import *
from Moon.python.Window import * # pyright: ignore
from Moon.python.Rendering.Shapes import * # pyright: ignore
from Moon.python.Math import distance

window = Window(1920, 1080, "Moon Framework Demo", context_settings=ContextSettings().set_antialiasing_level(8))
window_events = WindowEvents()


point_1 = Vector2f(200, 200)
point_2 = Vector2f(800, 500)

radius = 50


line = BaseLineShape()
line.set_points(point_1, point_2)

circle = CircleShape()
circle.set_outline_thickness(2)
circle.set_outline_color(COLOR_BLACK)
circle.set_color(COLOR_TRANSPARENT)
circle.set_origin_radius(radius)

clicked: int | None = None
draw_circle: int | None

while window.update(window_events):
    window.clear()

    if distance(MouseInterface.get_position_in_window(window), point_1) < radius:
        if MouseInterface.get_click('left'):
            clicked = 1
            draw_circle = 1
        draw_circle = 1

    if distance(MouseInterface.get_position_in_window(window), point_2) < radius:
        if MouseInterface.get_click('left'):
            clicked = 2
            draw_circle = 2
        draw_circle = 2


    if not MouseInterface.get_press('left'):
        clicked = None
        draw_circle = None


    ms = MouseInterface.get_speed()

    if clicked:
        if clicked == 1:
            point_1 += ms
        if clicked == 2:
            point_2 += ms


    line.set_points(point_1, point_2)
    window.draw(line)

    if draw_circle:
        pos = point_1 if draw_circle == 1 else point_2
        circle.set_position(pos)
        window.draw(circle)

    window.display()
