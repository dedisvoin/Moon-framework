import sys
sys.path.append("./")
from Moon.python.Window import *
from Moon.python.Rendering.Shapes import *
from Moon.python.Rendering.RenderStates import *
from Moon.python.Inputs import MouseInterface

window = Window(title="test").set_view_info()


events = WindowEvents()


circle = CircleShape(30)
circle.set_origin_radius(100)

rs = RenderStates()
rs.set_blend_mode(BlendMode(
    BlendMode.Factor.One,
    BlendMode.Factor.One,
    BlendMode.Equation.Subtract,
    BlendMode.Factor.One,
    BlendMode.Factor.One,
    BlendMode.Equation.Max,
))

while window.is_open():
    if not window.update(events): window.close()
    window.clear(COLOR_WHITE)

    circle.set_color(COLOR_RED.set_alpha(200))
    circle.set_position(400, 400)
    window.draw(circle)

    circle.set_color(COLOR_ORANGE.set_alpha(100))
    circle.set_position(MouseInterface.get_position_in_window(window))

    window.draw(circle, rs)


    window.view_info()
    window.display()
    
