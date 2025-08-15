import sys
sys.path.append("./")
from Moon.python.Window import *
from Moon.python.Rendering.Vertexes import *
from Moon.python.Rendering.RenderStates import *
from Moon.python.Rendering.Sprites import *
from Moon.python.Colors import *
from Moon.python.Vectors import *

window = Window()
events = WindowEvents()
window.set_view_info()

# Создаем массив вершин для квада
array = VertexArray()
array.set_primitive_type(VertexArray.PrimitiveType.QUADS)

# Добавляем вершины с текстурными координатами (белый цвет для правильного отображения текстуры)
white_color = Color(255, 255, 255, 255)
# Используем правильный метод append с объектом Vertex, содержащим текстурные координаты


array.append(Vertex(Vector2f(400, 400), white_color, Vector2f(0, 0)))  # Левый верхний
array.append(Vertex(Vector2f(800, 400), white_color, Vector2f(64, 0)))  # Правый верхний
array.append(Vertex(Vector2f(800, 800), white_color, Vector2f(64, 64)))  # Правый нижний
array.append(Vertex(Vector2f(400, 800), white_color, Vector2f(0, 64)))  # Левый нижний



def create_circle_texture(resolution: int = 64) -> RenderTexture:
    texture = RenderTexture().create(resolution, resolution)
    texture.clear(COLOR_TRANSPARENT)
    circle = CircleShape(30)

    circle.set_position(resolution / 2, resolution / 2)
    circle.set_origin_radius(resolution / 2)
    circle.set_color(COLOR_RED)

    texture.draw(circle)
    texture.display()
    return texture


image = create_circle_texture(64).get_texture()
# Создаем состояния рендеринга и устанавливаем текстуру
render_states = RenderStates()
render_states.set_texture(image)


while window.update(events):
    window.clear(COLOR_BLACK)
    
    # Проверяем с текстурой
    
    window.draw(array, render_states) 

    array.set_vertex_position(0, *MouseInterface.get_position_in_window(window).xy)
    
    window.view_info()
    window.display()