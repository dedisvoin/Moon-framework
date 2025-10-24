import sys
sys.path.append('./')

from Moon.python.Window import *
from Moon.python.Rendering.Sprites import *
from Moon.python.Rendering.Shapes import *
from Moon.python.Vectors import *

result, texture = Texture().load_from_file(r"demos\texture.png")


SCR = get_screen_resolution()


class Obj(object):
    def __init__(self):
        self.pos = Vector2f(1000, 800)
        self.speed = Vector2f.random() * random.uniform(0, 10)
        self.sprite = Sprite2D().link_texture(texture)
        self.sprite.set_scale(10).set_color(Color.random())

    def draw(self):
        window.draw(self.sprite)

    def update(self):
        self.pos += self.speed * window.get_delta()


        if self.pos.x <= 0 or self.pos.x >= SCR[0] - self.sprite.get_size().x:
            self.speed.x *= -1
            self.pos.x = max(0, min(self.pos.x, SCR[0] - self.sprite.get_size().x))
        if self.pos.y <= 0 or self.pos.y >= SCR[1] - self.sprite.get_size().y:
            self.speed.y *= -1
            self.pos.y = max(0, min(self.pos.y, SCR[1] - self.sprite.get_size().y))
        self.sprite.set_position(self.pos)
        #self.sprite.set_rotation(self.pos.x)



window = Window(title="Привeт",style=Window.Style.FullScreenDesktop, context_settings=ContextSettings().set_depth_bits(24).set_stencil_bits(8).set_antialiasing_level(4).set_opengl_version(3, 2))
window.set_wait_fps(FPS_UNLIMIT_CONST)
window_events = WindowEvents()
window.set_view_info()

arr = [Obj() for i in range(10000)]


while window.update(window_events):
    window.clear()

    for obj in arr:
        obj.update()
        obj.draw()
    window.view_info()

    window.display()
