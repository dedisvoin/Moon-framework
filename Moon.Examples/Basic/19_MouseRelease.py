import sys
sys.path.append("./")
from Moon.python.Window import *
from Moon.python.Inputs import *
from Moon.python.Rendering.Shapes import RectangleShape
from Moon.python.Rendering.Sprites import *
from Moon.python.Math import *
from Moon.python.Rendering.Text import Text



use_my_window = True

window = Window(style=Window.Style.No if use_my_window else Window.Style.Default)
window.enable_rounded_corners()
window.set_wait_fps(120)

header_height = 31
header = RectangleShape(1, 1)
header.set_color(window.get_header_color())
header_click = False


title_text = Text(Font.SystemFont("Calibri"))
title_text.set_size(16)
title_text.set_color(COLOR_WHITE)
title_text.set_text("Moon Engine")
title_text.set_origin(-8, -5)

events = WindowEvents()



right_resized = False
left_resized = False

close_sprite = LoadSprite(r'Moon\data\ui\close.png', 1)
close_sprite.set_typed_origin(OriginTypes.TOP_RIGHT)
close_sprite.set_color(COLOR_BLACK)
close_alpha = 255
close_target_alpha = 255
close_color = COLOR_RED.copy()

resize_sprite = LoadSprite(r'Moon\data\ui\resize.png', 1)
resize_sprite.set_typed_origin(OriginTypes.TOP_RIGHT)
resize_sprite.set_color(COLOR_BLACK)

red_rect = RectangleShape(50, 31).set_color(COLOR_RED)


cursor = SystemCursors.Arrow


win_size = [800, 600]
at_win_size = ...

while window.update(events):
    if use_my_window:
        #window.set_size(*win_size)
        win_size = [*window.get_size().xy]
        header.set_size(win_size[0], header_height)
        ms = MouseInterface.get_speed()
        cursor = SystemCursors.Arrow

        if point_in_rect(*MouseInterface.get_position_in_window(window).xy, 0, 0, win_size[0], header_height):
            
            if MouseInterface.get_press("left"):
                header_click = True
            else:
                header_click = False

            
        

        if point_in_rect(*MouseInterface.get_position_in_window(window).xy, win_size[0] - 5, 0, 10, win_size[1]):
            cursor = SystemCursors.SizeRight
            if MouseInterface.get_click("left"):
                right_resized = True
                
            
        
        if not MouseInterface.get_press("left"):
            header_click = False
            left_resized = False
            right_resized = False

        if right_resized:
            cursor = SystemCursors.SizeRight
            size = window.get_size()
            win_size[0] += ms.x
            window.set_size(*win_size)
            
            
        if header_click:
            cursor = SystemCursors.SizeAll
            window.set_position(*(window.get_position() + ms).xy)
        else:
            ...


        if point_in_rect(*MouseInterface.get_position_in_window(window).xy, window.get_size().x - red_rect.get_size().x, 0, *red_rect.get_size()):
            close_target_alpha = 255
            close_sprite.set_color(COLOR_WHITE)
            cursor = SystemCursors.Hand
            
        else:
            close_target_alpha = 0
            close_sprite.set_color(COLOR_BLACK)
            
        
        close_alpha += (close_target_alpha - close_alpha) * 0.2
        close_color.set_alpha(close_alpha)

        window.set_system_cursor(cursor)
        




    window.clear()
    if use_my_window:
        window.draw(header)
        window.draw(title_text)

        close_sprite.set_position(window.get_size().x, 3)
        red_rect.set_position(window.get_size().x - red_rect.get_size().x, 0).set_color(close_color)
        window.draw(red_rect)
        window.draw(close_sprite)

        resize_sprite.set_position(window.get_size().x - red_rect.get_size().x, 3)
        window.draw(resize_sprite)


    window.view_info()
    window.display()