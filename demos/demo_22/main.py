import sys
sys.path.append('./')
from Moon.python.Vectors import *
from Moon.python.Window import *
from Moon.python.Inputs import *
from Moon.python.Rendering.Shapes import *



# Инициализируем окно
window = Window(1000, 1000)
window.set_view_info()
window.set_wait_fps(160)
window.set_max_fps_history(40)
events = WindowEvents()


rect = RectangleShape(100, 100).set_color(COLOR_RED).set_position(200, 200).set_angle(60)

circle = CircleShape(10).set_origin_radius(100).set_color(COLOR_GREEN).set_position(200, 600)

line = LineShape().init_points().set_start_position(Vector2f(400, 400)).set_end_position(Vector2f(500, 800)).set_global_color(COLOR_CORAL)

polygone = PolygonShape()
polygone.set_global_color(COLOR_ORANGE)
polygone.add_vertex(Vector2f(400, 400))
polygone.add_vertex(Vector2f(800, 400))
polygone.add_vertex(Vector2f(600, 600))
polygone.set_all_vertices_colors([COLOR_RED, COLOR_GREEN, COLOR_BLUE])


print(circle)
print(line)
print(rect)
print(polygone)

while window.update(events):
    window.clear()
    window.draw(rect)
    window.draw(circle)
    window.draw(line)
    window.draw(polygone)



    window.view_info()
    window.display()
