import sys
sys.path.append("./")
from Moon.python.Window import *
from Moon.python.Colors import *
from Moon.python.Rendering.Shapes import *
from Moon.python.Rendering.RenderStates import *


# Создаем окно
window = Window(1200, 800, "Демонстрация Blend Режимов - PySGL")
events = WindowEvents()

# Создаем базовые объекты для демонстрации
background = RectangleShape(1200, 800).set_color(Color(50, 50, 50)).set_position(0, 0)

# Создаем цветные круги для демонстрации эффектов
red_circle = CircleShape(30).set_color(Color(255, 100, 100, 180)).set_position(200, 150).set_origin_radius(70)
green_circle = CircleShape(30).set_color(Color(100, 255, 100, 180)).set_position(250, 200).set_origin_radius(70)
blue_circle = CircleShape(30).set_color(Color(100, 100, 255, 180)).set_position(300, 150).set_origin_radius(70)

# Создаем прямоугольники для демонстрации различных blend режимов
demo_rects = []
blend_modes = [
    ("Alpha", BlendMode.Alpha()),
    ("Add", BlendMode.Add()),
    ("Multiply", BlendMode.Multiply()),
    ("Screen", BlendMode.Screen()),
    ("Subtract", BlendMode.Subtract()),
    ("Lighten", BlendMode.Lighten()),
    ("Darken", BlendMode.Darken()),
]

# Создаем демонстрационные области
for i, (name, blend_mode) in enumerate(blend_modes):
    x = 50 + (i % 4) * 280
    y = 350 + (i // 4) * 200
    
    # Фоновый прямоугольник
    bg_rect = RectangleShape(250, 150).set_color(Color(80, 80, 120)).set_position(x, y)
    
    # Перекрывающиеся цветные прямоугольники для демонстрации blend эффекта
    rect1 = RectangleShape(100, 100).set_color(Color(255, 150, 150, 200)).set_position(x + 30, y + 25)
    rect2 = RectangleShape(100, 100).set_color(Color(150, 255, 150, 200)).set_position(x + 80, y + 50)
    rect3 = RectangleShape(100, 100).set_color(Color(150, 150, 255, 200)).set_position(x + 55, y + 75)
    
    demo_rects.append((name, bg_rect, rect1, rect2, rect3, blend_mode))

# Создаем текст для подписей
from Moon.python.Rendering.Text import *
font = Font.SystemFont("arial")
title_text = BaseText(font).set_size(24).set_color(COLOR_WHITE).set_position(50, 20)
title_text.set_text("Blend Modes Demo")

info_text = BaseText(font).set_size(16).set_color(Color(200, 200, 200)).set_position(50, 60)
info_text.set_text("Each mode shows how overlapping colored rectangles blend together")

# Переменные для интерактивности
current_mode = 2
show_labels = True

while window.update(events):
    # Обработка событий
    if events.get_type() == events.Type.MouseWheelMoved:
        current_mode = (current_mode + events.get_mouse_wheel()) % len(blend_modes)
    
    # Рендеринг
    window.clear(Color(30, 30, 30))
    
    # Рисуем фон
    window.draw(background)
    
    # Рисуем заголовок и информацию
    window.draw(title_text)
    window.draw(info_text)
    
    # Демонстрация всех blend режимов в верхней части
    demo_bg = RectangleShape(400, 200).set_color(Color(60, 60, 80)).set_position(450, 100)
    window.draw(demo_bg)
    
    # Рисуем перекрывающиеся круги с текущим выбранным режимом
    current_blend_name, current_blend_mode = blend_modes[current_mode]
    blend_states = RenderStates().set_blend_mode(current_blend_mode)
    
    # Базовый слой
    base_circle = CircleShape(60).set_color(Color(100, 100, 100)).set_position(500, 150)
    window.draw(base_circle)
    
    # Цветные круги с blend эффектом
    window.draw(red_circle, blend_states)
    window.draw(green_circle, blend_states)
    window.draw(blue_circle, blend_states)
    
    # Подпись текущего режима
    mode_text = BaseText(font).set_size(20).set_color(COLOR_YELLOW).set_position(500, 320)
    mode_text.set_text(f"Current mode: {current_blend_name}")
    window.draw(mode_text)
    
    # Рисуем все демонстрационные области
    for i, (name, bg_rect, rect1, rect2, rect3, blend_mode) in enumerate(demo_rects):
        # Фон области
        window.draw(bg_rect)
        
        # Создаем состояния рендеринга для этого blend режима
        states = RenderStates().set_blend_mode(blend_mode)
        
        # Рисуем перекрывающиеся прямоугольники
        window.draw(rect1, states)
        window.draw(rect2, states)
        window.draw(rect3, states)
        
        # Подпись режима
        if show_labels:
            label_text = BaseText(font).set_size(14).set_color(COLOR_WHITE)
            label_text.set_position(bg_rect.get_position().x + 10, bg_rect.get_position().y + 5)
            label_text.set_text(name)
            window.draw(label_text)
        
        # Выделяем текущий выбранный режим
        if i == current_mode:
            highlight = RectangleShape(254, 154).set_color(Color(255, 255, 0, 0))
            highlight.set_outline_thickness(2).set_outline_color(COLOR_YELLOW)
            highlight.set_position(bg_rect.get_position().x - 2, bg_rect.get_position().y - 2)
            window.draw(highlight)

    
    window.view_info()
    window.display()