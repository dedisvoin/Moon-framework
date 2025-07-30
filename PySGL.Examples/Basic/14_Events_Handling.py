import sys
sys.path.append("./")
from PySGL.python.Window import *
from PySGL.python.Colors import *
from PySGL.python.Rendering.Shapes import *

# Создаем окно с отладочной информацией
window = Window(800, 600, "События и ввод - PySGL").set_view_info()
events = WindowEvents()

# Создаем объекты для демонстрации
circle = CircleShape(30).set_color(COLOR_BLUE).set_position(400, 300)
rect = RectangleShape(60, 40).set_color(COLOR_RED).set_position(100, 100)

# Переменные состояния
mouse_pressed = False
key_info = "Нажмите любую клавишу"
mouse_info = "Кликните мышью"

while window.update(events):
    # Обработка событий
    event_type = events.get_type()
    
    # Обработка событий клавиатуры
    if event_type == WindowEvents.Type.KeyPressed:
        key_code = events.get_key()
        key_info = f"Нажата клавиша: {key_code}"
        
    # Обработка событий мыши
    elif event_type == WindowEvents.Type.MouseButtonPressed:
        button = events.get_mouse_button()
        x, y = events.get_mouse_x(), events.get_mouse_y()
        mouse_info = f"Кнопка {button} в ({x}, {y})"
        mouse_pressed = True
        # Перемещаем круг к позиции клика
        circle.set_position(x, y)
        
    elif event_type == WindowEvents.Type.MouseButtonReleased:
        mouse_pressed = False
        
    elif event_type == WindowEvents.Type.MouseMoved:
        if mouse_pressed:
            x, y = events.get_mouse_x(), events.get_mouse_y()
            circle.set_position(x, y)
            
    # Обработка изменения размера окна
    elif event_type == WindowEvents.Type.Resized:
        new_width = events.get_size_width()
        new_height = events.get_size_height()
        print(f"Окно изменено: {new_width}x{new_height}")
    
    # Рендеринг
    window.clear(COLOR_WHITE)
    window.draw(circle)
    window.draw(rect)
    window.view_info()
    window.display()