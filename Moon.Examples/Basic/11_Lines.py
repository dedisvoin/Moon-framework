import sys
sys.path.append("./")
from Moon.python.Window import *
from Moon.python.Colors import *
from Moon.python.Rendering.Shapes import *
from Moon.python.Math import distance


from dataclasses import dataclass

window = Window(style=Window.Style.FullScreenDesktop).set_view_info()
window.set_wait_fps(6000)
events = WindowEvents()



@dataclass
class Point:
    rect: RectangleShape
    pos: Vector2f
    speed: Vector2f
    id: str


rects: list[Point] = []

def uppend_rect(count):
    global rects
    for _ in range(count):
        p = Point(RectangleShape(10, 10).set_color(COLOR_BLACK).set_origin(5, 5).set_angle(random.randint(0, 360)),
                  Vector2f(random.randint(0, 1920), random.randint(0, 1080)),
                  Vector2f(random.randint(-5, 5), random.randint(-5, 5)), str(uuid4()))
        
        rects.append(p)
        
        
line = LineShape()
line.set_rounded()
line.set_color(COLOR_LIGHT_GRAY)

        
def render():
    for rect in rects:
        
        
        for rect2 in rects:
            if rect2.id != rect.id and distance(rect.pos, rect2.pos) <= 100:
                line.set_points(rect.pos, rect2.pos)
                line.set_width((1 - distance(rect.pos, rect2.pos) / 100) * 10)
                window.draw(line)
                break
            
    for rect in rects:
        rect.rect.set_position(rect.pos)
        window.draw(rect.rect)
        
        
        
        
        
def update():
    global rects
    screen_width = window.get_size().x
    screen_height = window.get_size().y
    
    for point in rects:
        # Обновляем позицию
        point.pos.x += point.speed.x * window.get_render_time(60)
        point.pos.y += point.speed.y * window.get_render_time(60)
        
        # Проверяем столкновение с границами экрана
        if point.pos.x <= 0 or point.pos.x >= screen_width - point.rect.get_size().x:
            point.speed.x *= -1  # Отскок по горизонтали
            # Корректировка позиции, чтобы не застревать за границей
            point.pos.x = max(0, min(point.pos.x, screen_width - point.rect.get_size().x))
            
        if point.pos.y <= 0 or point.pos.y >= screen_height - point.rect.get_size().y:
            point.speed.y *= -1  # Отскок по вертикали
            # Корректировка позиции
            point.pos.y = max(0, min(point.pos.y, screen_height - point.rect.get_size().y))
            

uppend_rect(200)
while window.update(events):

    window.clear(COLOR_DARK_GRAY)
    
    render()
    update()

    window.view_info()
    window.display()

