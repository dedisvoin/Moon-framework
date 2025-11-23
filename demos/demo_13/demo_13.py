import sys
sys.path.append('./')

from Moon.python.Inputs import *
from Moon.python.Window import *
from Moon.python.Rendering.Vertexes import *
from Moon.python.Rendering.Shapes import *
from Moon.python.Threader import CycleWorker

window = Window(title="Test")
window.set_wait_fps(FPS_VSYNC_CONST)
window.set_view_info()
window_events = WindowEvents()


window.set_system_cursor(SystemCursors.SizeAll)

array = VertexList(0)
array.set_primitive_type(VertexListTypes.TriangleFan)


rect = RectangleShape()
rect.set_outline_color(COLOR_YELLOW).set_color(COLOR_YELLOW.copy().set_alpha_float(0.1)).set_outline_thickness(2)




def print_count(worker: CycleWorker):
    if window.is_shutting_down() is True: # Завершаем работу воркера, если окно в процессе закрытия
        worker.stop() # Останавливаем воркер
        return
    print("Vertex count:", array.length())
    


worker = CycleWorker()
worker.set_delay(0.5)
worker.start(print_count)

while window.update(window_events):
    window.clear()


    if MouseInterface.get_press('left'):
        color = Color(100, 200, 150)
        array.auto_append(Vertex2d().FromPositionAndColor(MouseInterface.get_position_in_window(window), color))
    if MouseInterface.get_press('right'):
        array.remove(0)

    window.draw(array)

    pos, size = array.get_local_bound()
    if pos is not None and size is not None:
        rect.set_position(pos).set_size(size)

    window.draw(rect)
    window.view_info()

    window.display()

# window.close() # Принудительно закрывает окно и завершает все связанные процессы в том числе воркеры
# worker.stop() # Останавливает воркер если он еще работает
