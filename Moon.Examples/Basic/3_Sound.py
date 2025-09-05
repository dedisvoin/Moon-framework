import sys
import random
sys.path.append("./")
from Moon.python.Window import *
from Moon.python.Inputs import MouseInterface
from Moon.python.Audio import *
from Moon.python.Rendering.Text import *


window = Window().set_view_info()
events = WindowEvents()
window.set_wait_fps(FPS_UNLIMIT_CONST)
sound = MultiSound(Sound(SoundBuffer("game_data\wall.wav")), 70)

class KickObject:
    def __init__(self, volume: int, position, color):
        self.__radius = 1
        self.__alpha = 255
        self.__color = color.copy()
        self.__position = position

    @property
    def alpha(self) -> float:
        return self.__alpha

    def update(self, render_time: float):
        self.__radius += 0.5 * render_time * 1000
        self.__alpha -= 0.628318 * render_time * 1000  # 2*pi/10

    def render(self):
        self.__color.set_alpha(self.__alpha)
        CIRCLE_SHAPE.set_color(self.__color)
        CIRCLE_SHAPE.set_origin_radius(self.__radius)
        CIRCLE_SHAPE.set_position(*self.__position.xy)
        window.draw(CIRCLE_SHAPE)

KickObjectsPool = []

class Ball:
    def __init__(self):
        self.__color = Color.random().set_alpha_float(1)
        self.__position = window.get_center()
        self.__speed = Vector2f(random.randint(-1000, 1000), random.randint(-1000, 1000))
        self.__radius = random.randint(20, 100)
    
    def __handle_collision(self, axis, boundary, direction):
        sound.set_volume_current(self.__radius)
        sound.set_pitch_current(self.__radius / 100)
        sound.auto_play()
        
        if axis == 'x':
            self.__speed.x *= -1
            self.__position.x = boundary
            offset = Vector2f(self.__radius * direction, 0)
        else:
            self.__speed.y *= -1
            self.__position.y = boundary
            offset = Vector2f(0, self.__radius * direction)
            
        KickObjectsPool.append(KickObject(self.__radius, self.__position + offset, self.__color))
    
    def render(self):
        CIRCLE_SHAPE.set_origin_radius(self.__radius)
        CIRCLE_SHAPE.set_color(self.__color)
        CIRCLE_SHAPE.set_position(*self.__position.xy)
        window.draw(CIRCLE_SHAPE)

    def update(self, render_time: float):
        global KickObjectsPool
        self.__position += self.__speed * render_time
        
        # Check wall collisions
        if self.__position.x - self.__radius <= 0:
            self.__handle_collision('x', self.__radius, -1)
        elif self.__position.x + self.__radius >= window.get_size().x:
            self.__handle_collision('x', window.get_size().x - self.__radius, 1)
            
        if self.__position.y - self.__radius <= 0:
            self.__handle_collision('y', self.__radius, -1)
        elif self.__position.y + self.__radius >= window.get_size().y:
            self.__handle_collision('y', window.get_size().y - self.__radius, 1)


try:
    ball_count = int(input("Enter ball count [default 3]: ") or 3)
except ValueError:
    ball_count = 3
balls = [Ball() for _ in range(ball_count)]


while window.update(events):

    for ball in balls:
        ball.update(window.get_render_time())
    
    for obj in KickObjectsPool:
        obj.update(window.get_render_time())
    
    KickObjectsPool = [obj for obj in KickObjectsPool if obj.alpha >= 1]
    

    window.clear()
    for ball in balls:
        ball.render()
    for obj in KickObjectsPool:
        obj.render()
    
    window.view_info()
    window.display()