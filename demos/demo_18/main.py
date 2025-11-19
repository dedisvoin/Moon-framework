import sys
sys.path.append('./')
import time # Нам нужен модуль time для передачи 'iTime'

from Moon.python.Vectors import *
from Moon.python.Window import *
from Moon.python.Rendering.Shaders import *
from Moon.python.Rendering.Sprites import *
from Moon.python.Inputs import *
from Moon.python.System import *

# Инициализируем окно
window = Window(1000, 1000)
window.set_view_info()
window.set_wait_fps(FPS_VSYNC_CONST)
events = WindowEvents()

print(get_gpu_version())
print(get_gpu_vendor())
print(get_gpu_renderer())
print(get_cpu())
print(get_cpu_count())
print(get_cpu_count(1))
print(get_cpu_freq())
print(get_cpu_freq_max())
print(get_cpu_freq_min())
print(get_cpu_cores_percent(1))
print(get_cpu_percent(1))
# --- Код круга и RenderTexture удален, он не нужен ---
# Этому шейдеру нужен только "холст" (Sprite2D), на котором он будет рисоваться.
# Создаем простой спрайт, который будет растягиваться на весь экран.

texture = RenderTexture().Init(1000, 1000)
fullscreen_quad = Sprite2D().link_render_texture(texture)


# --- Загружаем Шейдер "Cairo" ---


# Загружаем шейдер
cairo_shader = Shader.LoadFromFiles(
    vertex_path='demos/demo_18/vertex.glsl',
    fragment_path='demos/demo_18/fragment.glsl'
)


# Запоминаем время старта
start_time = time.time()


# --- Главный цикл ---
while window.update(events):
    window.clear()

    # Получаем текущие размеры окна
    window_width, window_height = window.get_size()

    if window.get_resized():
        # Обновляем размер нашего "холста"
        texture = RenderTexture().Init(*window.get_size())
        fullscreen_quad.link_render_texture(texture, True)

    # Считаем текущее время
    current_time = time.time() - start_time
    
    # Получаем позицию мыши
    mouse_pos = MouseInterface.get_position_in_window(window).to_float()

    # --- Передаем данные в шейдер ---
    cairo_shader.set_uniform("resolution", Vector2f(window_width, window_height))
    cairo_shader.set_uniform("time", current_time * 20)
    cairo_shader.set_uniform("mouse", mouse_pos * 200) # Передаем как Vector2i

    # --- Рендер ---
    # Рисуем наш полноэкранный спрайт с применением шейдера
    window.draw(fullscreen_quad, cairo_shader)

    window.view_info()
    window.display()