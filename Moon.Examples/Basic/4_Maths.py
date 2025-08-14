import sys
sys.path.append("./")
from Moon.python.Window import *
from Moon.python.Rendering.Shapes import *
from Moon.python.Math import *

from Moon.python.Inputs import MouseInterface

window = Window().set_view_info().set_wait_fps(60)
events = WindowEvents()



line_1_points = [
    [300, 300], [700, 400]
]

LINE_THIN_SHAPE.set_start_point(*line_1_points[0])
LINE_THIN_SHAPE.set_end_point(*line_1_points[1])

vector_position = Vector2f(400, 200)
vector = Vector2f(0, 300)
vector_line = LineThinShape()
intersection_circle = CircleShape(10)
intersection_circle.set_origin_radius(8)
intersection_circle.set_color(COLOR_RED)




while window.update(events):
    alpha = 255 * abs(math.sin(window.get_global_timer()))

    window.set_alpha(alpha)
    

    window.clear()

    window.draw(LINE_THIN_SHAPE)
    if point_on_line_segment(*MouseInterface.get_position_in_window(window).xy, *line_1_points[0], *line_1_points[1], 2):
        intersection_circle.set_color(COLOR_GREEN)
        intersection_circle.set_position(*MouseInterface.get_position_in_window(window).xy)
        window.draw(intersection_circle)

    vector.rotate_at(50 * window.get_render_time())
    vector_line.set_start_point(*vector_position.xy)
    vector_line.set_end_point(*(vector_position + vector))
    window.draw(vector_line) 
    if pos:=line_intersection(*line_1_points[0], *line_1_points[1], *vector_position.xy, *(vector_position + vector)):
        intersection_circle.set_color(COLOR_RED)
        intersection_circle.set_position(*pos)
        window.draw(intersection_circle)

    window.view_info()
    window.display()
