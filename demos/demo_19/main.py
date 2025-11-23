import sys
sys.path.append('./')
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

# Загружаем шейдер
shader = Shader().LoadFragmentFromFile(r"Moon\shaders\blur\gaus_blur.frag")

# Создаем объекты
circle = CircleShape(30).set_color(Color(255, 200, 100, 255))

rect = RectangleShape(200, 100).set_color(COLOR_RED).set_position(200, 100)

# Текстуры для эффекта
surface = RenderTexture2D().Init(1000, 1000)
surface_sprite = Sprite2D().link_render_texture(surface)

bloom_texture = RenderTexture2D().Init(1000, 1000)
bloom_sprite = Sprite2D().link_render_texture(bloom_texture)

output_texture = RenderTexture2D().Init(1000, 1000)
output_sprite = Sprite2D().link_render_texture(output_texture)

def render_bloom():
    # ПРОХОД 1: Создаем bloom эффект
    bloom_texture.clear(COLOR_BLACK)
    
    shader.set_uniform('textureSize', Vector2f(1000, 1000))
    shader.set_uniform('intensity', 10)    # Сила свечения
    shader.set_uniform('radius', 100)       # Радиус размытия
    
    bloom_texture.draw(surface_sprite, shader)
    bloom_texture.display()
    
    # ПРОХОД 2: Комбинируем оригинал + bloom
    output_texture.clear(COLOR_BLACK)
    output_texture.draw(surface_sprite)     # Оригинальный круг
    output_texture.draw(bloom_sprite)       # Свечение поверх
    output_texture.display()

# Главный цикл
while window.update(events):
    window.clear(COLOR_BLACK)

    # Рендерим сцену
    surface.clear(COLOR_BLACK)
    surface.draw(circle.set_position(MouseInterface.get_position_in_window(window)).set_color(COLOR_ORANGE).set_origin_radius(100))
    surface.draw(circle.set_position(Vector2f(500, 500)).set_color(COLOR_GREEN).set_origin_radius(50))
    surface.draw(rect)
    surface.display()

    # Применяем bloom эффект
    render_bloom()
    
    # Выводим результат
    window.draw(output_sprite)
    window.view_info()
    window.display()