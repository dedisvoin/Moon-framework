import sys
sys.path.append("./")
from Moon.python.Window import *
from Moon.python.Rendering.Shapes import *

window = Window(title="test").set_view_info()
window.set_wait_fps(60)

events = WindowEvents()


vector = Vector2f(100, 0)
pos = Vector2f(400, 400)

thin = LineThinShape()
thin.set_color(COLOR_RED)

while window.is_open():
    if not window.update(events): window.close()
    window.clear()

    vector.set_angle(vector.get_angle() + 1)
    thin.set_points(*pos, *(pos + vector))


    window.draw(thin)

    window.view_info()
    window.display()
    
