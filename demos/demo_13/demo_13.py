import sys
sys.path.append('./')


from Moon.python.Inputs import *
from Moon.python.Window import *
from Moon.python.Rendering.Vertexes import *

window = Window(title="Test")
window.set_wait_fps(FPS_VSYNC_CONST)
window.set_view_info()
window_events = WindowEvents()


window.set_system_cursor(SystemCursors.SizeAll)

array = VertexList(0)
array.set_primitive_type(VertexListTypes.TriangleFan)

while window.update(window_events):
    window.clear()


    if MouseInterface.get_press('left'):
        color = Color(100, 200, 150)
        array.auto_append(Vertex2d().FromPositionAndColor(MouseInterface.get_position_in_window(window), color))
    if MouseInterface.get_press('right'):
        array.remove(0)
    window.draw(array)
    window.view_info()

    window.display()
