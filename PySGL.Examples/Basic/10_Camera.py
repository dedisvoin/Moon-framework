import sys
sys.path.append("./")
from PySGL.python.Window import *
from PySGL.python.Engine.Camera import *
from PySGL.python.Rendering.Shapes import *
from PySGL.python.Vectors import Vector2f

# Создание окна с улучшенными настройками
window = Window().set_view_info()
window.set_wait_fps(60)
window.set_vertical_sync(True)

events = WindowEvents()
window.set_system_cursor(SystemCursors.Hand)
window.enable_rounded_corners()

# Создание объектов для отрисовки
rect = RectangleShape(100, 36)
rect.set_color(COLOR_RED)
rect.set_outline_color(COLOR_BLACK)
rect.set_outline_thickness(1)
rect.set_position(150, 100)

# Создание камеры с улучшенными настройками
camera = Camera2D(800, 600)
camera.set_window(window)
camera.set_lerp_movement(0.05)  # Плавное движение
camera.set_lerp_zoom(0.03)      # Плавный зум
camera.set_target_zoom(1.2)     # Небольшое увеличение

# Позиция для следования камеры
target_pos = Vector2f(150, 100)
frame_count = 0

print("Демонстрация камеры с улучшенным модулем Views")
print("Камера следует за вращающимся прямоугольником")
print("Нажмите ESC для выхода")

while window.is_open():
    if not window.update(events): 
        window.close()
    
    window.clear()
    
    # Обновляем позицию цели (круговое движение)
    import math
    frame_count += 1
    angle = frame_count * 0.02
    target_pos.x = 400 + math.cos(angle) * 200
    target_pos.y = 300 + math.sin(angle) * 150
    
    # Камера следует за целью
    camera.follow(target_pos)
    
    # Добавляем тряску каждые 3 секунды
    if frame_count % 180 == 0:
        camera.shake(5)
    
    # Применяем камеру и обновляем
    camera.apply(window)
    camera.update()
    
    # Обновляем объект
    rect.set_position(*target_pos.as_tuple())
    rect.set_angle(rect.get_angle() + 2)
    
    # Отрисовка
    window.draw(rect)
    
    # Информация о камере
    view = camera.get_view()
    center = view.get_center()
    zoom = camera.get_zoom()
    
    # Возвращаем стандартный вид для UI
    camera.reapply(window)
    
    window.view_info()
    window.display()

print("Демонстрация завершена")
    
