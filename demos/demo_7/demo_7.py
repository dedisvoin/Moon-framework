import sys
sys.path.append('./')


from Moon.python.Inputs import *
from Moon.python.Window import * # pyright: ignore
from Moon.python.Rendering.Shapes import * # pyright: ignore
from Moon.python.Audio import *  # pyright: ignore
from Moon.python.Vectors import *
from Moon.python.Microphone import *

window = Window(title = "Moon Framework Demo", context_settings=ContextSettings().set_antialiasing_level(8))
window_events = WindowEvents()



pos = window.get_center()
speed = Vec2f(0, 0)

gravity = Vec2f(0, 2)


circle = CircleShape()
circle.set_color(COLOR_RED)
circle.set_origin_radius(100)


mic = SimpleMicrophone()
mic.start()

volumes = []

v_rect = RectangleShape(1, 1)
v_rect.set_color(COLOR_RED)
v_rect.set_size(10, 0)

while window.update(window_events):
    window.clear()

    speed += gravity
    pos += speed

    if pos.y + 100 >= window.get_height():
        speed.y *= -0.6
        pos.y = window.get_height() - 100
        speed.x *= 0.9



    if pos.x - 100 <= 0:
        pos.x = 100
        speed.x *= -0.8
    if pos.x + 100 >= window.get_width():
        pos.x = window.get_width() - 100
        speed.x *= -0.8

    if mic.is_volume_increased(0.01):
        speed = Vec2f(random.randint(-5, 5), -mic.get_volume_difference() * 10 * 50)



    volumes.append(mic.get_pitch())
    if len(volumes) > 300: volumes.pop(0)

    for x, v in enumerate(volumes):
        v_rect.set_position(0 + x * 2, 0)
        v_rect.set_size(2, abs(v))
        window.draw(v_rect)

    #print(mic.get_pitch())
    print(mic.get_pitch_note())


    circle.set_position(pos)
    window.draw(circle)

    window.display()
