import sys
sys.path.append('./')
from Moon.python.Vectors import *
from Moon.python.Window import *
from Moon.python.Rendering.Shapes import *
from Moon.python.Threader import *
from Moon.python.System import *


window = Window(1000, 1000, style=Window.Style.Close)
window.set_view_info()
window.set_wait_fps(FPS_VSYNC_CONST)
events = WindowEvents()

polygone = PolygonShape()
polygone.add_vertex(Vector2f(200, 200))
polygone.add_vertex(Vector2f(800, 200))
polygone.add_vertex(Vector2f(500, 800))
polygone.set_all_vertices_colors([COLOR_RED, COLOR_GREEN, COLOR_BLUE])

print(get_base_dir())
print(get_base_path())
resize_width = False
resize_height = False
resize_all = False

lock = Lock()
sync = True

def update(worker: CycleWorker):
    global resize_width, resize_height, resize_all
    mp = MouseInterface.get_position_in_window(window)

    dx = abs(mp.x - window.get_width())
    dy = abs(mp.y - window.get_height())



    
    window.set_system_cursor(SystemCursors.Arrow)
    if dx <= 5 and dy >= 10:
        window.set_system_cursor(SystemCursors.SizeHorizontal)
        if MouseInterface.get_click('left'):
            resize_width = True

    if not MouseInterface.get_press('left'):
        resize_width = False

    if resize_width:
        window.set_size(abs(window.get_position().x - MouseInterface.get_position().x), window.get_height())

    if dy <= 5 and dx >= 10:
        window.set_system_cursor(SystemCursors.SizeVertical)
        if MouseInterface.get_click('left'):
            resize_height = True

    if not MouseInterface.get_press('left'):
        resize_height = False

    if resize_height:
        window.set_size(window.get_width(), abs(window.get_position().y - MouseInterface.get_position().y) - 40)

    if dy <= 5 and dx <= 5:
        window.set_system_cursor(SystemCursors.SizeBottomRight)
        if MouseInterface.get_click('left'):
            resize_all = True

    if not MouseInterface.get_press('left'):
        resize_all = False

    if resize_all:
        window.set_size(abs(window.get_position().x - MouseInterface.get_position().x), abs(window.get_position().y - MouseInterface.get_position().y) - 40)
    
            
update_worker = CycleWorker()
update_worker.set_delay(1/180)
update_worker.start(update)


while window.update(events):
    window.clear()
    window.draw(polygone)
    polygone.get_vertex(0).position = Vector2f(200, 200)
    polygone.get_vertex(1).position = Vector2f(window.get_width() - 200, 200)
    polygone.get_vertex(2).position = Vector2f(window.get_width() / 2, window.get_height() - 200)
    
    window.view_info()
    window.display()


window.close()
update_worker.stop()
