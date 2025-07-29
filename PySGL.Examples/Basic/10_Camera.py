import sys
sys.path.append("./")
from PySGL.python.Window import *
from PySGL.python.Engine.Camera import *
from PySGL.python.Rendering.Shapes import *

window = Window().set_view_info()
window.set_wait_fps(60)
window.set_vertical_sync(True)

events = WindowEvents()
window.set_system_cursor(SystemCursors.Hand)
window.enable_rounded_corners()

rect = RectangleShape(100, 36)
rect.set_color(COLOR_RED)
rect.set_outline_color(COLOR_BLACK)
rect.set_outline_thickness(1)
rect.set_position(150, 100)


camera = Camera2D(800, 600)
camera.set_window(window)






while window.is_open():
    if not window.update(events): window.close()
    window.clear()
    camera.apply(window)
    camera.update()

    rect.set_angle(rect.get_angle() + 5)
    window.draw(rect)
    window.view_info()
    window.display()
    
