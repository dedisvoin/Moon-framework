import sys
sys.path.append("./")
from Moon.python.Window import *
from Moon.python.Colors import *
from Moon.python.Rendering.Shapes import *

# Создаем настройки контекста с антиалиасингом
context_settings = ContextSettings()
context_settings.set_antialiasing_level(16)  # Высокий уровень сглаживания
context_settings.set_depth_bits(24)         # 24-битный буфер глубины
context_settings.set_opengl_version(3, 3)   # OpenGL 3.3
context_settings.set_srgb_capable(True)     # Поддержка sRGB

# Создаем окно с кастомными настройками
window = Window(800, 600, "Настройки контекста - PySGL", 
               context_settings=context_settings).set_view_info()
window.set_wait_fps(FPS_UNLIMIT_CONST)
events = WindowEvents()

# Создаем фигуры для демонстрации антиалиасинга
shapes = []
for i in range(5):
    circle = CircleShape(10 + i * 10)
    circle.set_color(Color(255 - i * 40, 100 + i * 30, 50 + i * 40))
    circle.set_position(150 + i * 120, 200)
    circle.set_outline_thickness(3)
    circle.set_outline_color(COLOR_BLACK)
    shapes.append(circle)

# Линии для демонстрации сглаживания
lines = []
for i in range(10):
    line = LineShape()
    line.set_start_point(50, 400 + i * 15)
    line.set_end_point(750, 450 + i * 10)
    line.set_width(2 + i)
    line.set_color(Color(255, 100 + i * 15, 100))
    lines.append(line)

rotation = 0

while window.update(events):
    rotation += 50 * window.get_render_time()
    
    # Вращаем фигуры для демонстрации сглаживания
    for i, shape in enumerate(shapes):
        shape.set_angle(rotation + i * 30)
    
    window.clear(COLOR_WHITE)
    
    # Рисуем все фигуры
    for shape in shapes:
        window.draw(shape)
    for line in lines:
        window.draw(line)
    
    window.view_info()
    window.display()