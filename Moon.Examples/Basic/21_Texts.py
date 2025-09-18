import sys
sys.path.append("./")
from Moon.python.Window import *
from Moon.python.Rendering.Text import *
from Moon.python.Inputs import *
from Moon.python.Rendering import Shapes
from Moon.python.Rendering.Shapes import RectangleShape
import time

init_system_fonts()

font = get_system_font_with_name("calibri")


text_obj = Text(font)
text_obj.set_color(COLOR_BLACK)

text_obj.set_outline_thickness(0)
text_obj.set_size(50)
text_obj.set_text("")

# Создаем каретку (текстовый курсор)
caret = RectangleShape(2, 50)
caret.set_color(COLOR_BLACK)
caret_visible = True
caret_blink_time = 0.5  # Время мигания в секундах
last_blink_time = time.time()
cursor_position = 0  # Позиция курсора в тексте


print(get_keyboard_layout())


window = Window()
window.set_view_info()
window.set_wait_fps(FPS_UNLIMIT_CONST)

events = WindowEvents()
while window.update(events):
    window.clear()
    text_obj.set_position(*window.get_center().xy)
    text_obj.set_outline_color(get_rainbow_with_time(window.get_global_timer(0.5)))

    # Обработка мигания каретки
    current_time = time.time()
    if current_time - last_blink_time > caret_blink_time:
        caret_visible = not caret_visible
        last_blink_time = current_time

    if KeyBoardInterface.get_click_any():
        key = KeyBoardInterface.get_pressed_keys()

        if len(key) == 1:
            current_text = text_obj.get_text()

            if key[0] == 'backspace':
                if cursor_position > 0:
                    text_obj.set_text(current_text[:cursor_position-1] + current_text[cursor_position:])
                    cursor_position -= 1
            elif key[0] == 'space':
                text_obj.set_text(current_text[:cursor_position] + ' ' + current_text[cursor_position:])
                cursor_position += 1
            elif key[0] == 'enter':
                text_obj.set_text(current_text[:cursor_position] + '\n' + current_text[cursor_position:])
                cursor_position += 1
            elif key[0] == 'left' and cursor_position > 0:
                cursor_position -= 1
            elif key[0] == 'right' and cursor_position < len(current_text):
                cursor_position += 1
            elif key[0] in Keyboard.CHAR_SET:
                text_obj.set_text(current_text[:cursor_position] + key[0] + current_text[cursor_position:])
                cursor_position += 1

            text_obj.set_letter_spacing(3)
            text_obj.set_typed_origin(OriginTypes.CENTER)
            text_obj.set_text_scale(1)
            caret_visible = True  # Сбрасываем мигание при нажатии клавиши
            last_blink_time = current_time

        elif len(key) == 2:
            print(key)
            current_text = text_obj.get_text()

            if 'shift' in key:
                i = key.index('shift')
                key = key[i-1]
                text_obj.set_text(current_text[:cursor_position] + key.upper() + current_text[cursor_position:])
                cursor_position += 1

                text_obj.set_letter_spacing(3)
                text_obj.set_typed_origin(OriginTypes.CENTER)
                text_obj.set_text_scale(1)
                caret_visible = True  # Сбрасываем мигание при нажатии клавиши
                last_blink_time = current_time



    window.draw(text_obj)

    # Отрисовка каретки
    if caret_visible:
        # Расчет положения каретки
        current_text = text_obj.get_text()
        text_width = 0

        if cursor_position > 0:
            # Измеряем ширину текста до позиции курсора
            temp_text = Text(font)
            temp_text.set_size(50)
            temp_text.set_letter_spacing(3)
            temp_text.set_text(current_text[:cursor_position])
            text_width = temp_text.get_text_width()

        # Устанавливаем позицию каретки
        center_x, center_y = window.get_center().xy
        caret.set_position(center_x - text_obj.get_text_width()/2 + text_width + 3, center_y - 10)

        # Рисуем каретку
        window.draw(caret)

    window.view_info()
    window.display()
