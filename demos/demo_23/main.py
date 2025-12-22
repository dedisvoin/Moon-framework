import sys
sys.path.append('./')
from Moon.python.Vectors import *
from Moon.python.Window import *
from Moon.python.Inputs import *
from Moon.python.Rendering.Shapes import *
from Moon.python.Rendering.Sprites import *
from Moon.python.Threader import CycleWorker


# Инициализируем окно
window = Window(1000, 1000, dynamic_update=True)
window.set_view_info()
window.set_wait_fps(160)
events = WindowEvents()


circle = CircleShape().set_color(COLOR_RED).set_origin_radius(5)


grass_textures = [
    Texture2D().load_from_file(r"demos\demo_23\data\grass_1.png")[-1].set_smooth(False),
    Texture2D().load_from_file(r"demos\demo_23\data\grass_2.png")[-1].set_smooth(False),
    Texture2D().load_from_file(r"demos\demo_23\data\grass_3.png")[-1].set_smooth(False)
]

class MySprite(Sprite2D):
    def __init__(self, saved_pos):
        super().__init__()
        self.saved_pos = saved_pos
        self.saved_angle = 0
        self.angle = 180

sprites_array: list[MySprite] = []

def draw_grass(grid_size, offset):
    global sprites_array

    if MouseInterface.get_press('left'):
        mouse_pos = MouseInterface.get_position_in_window(window).as_list()
        mouse_pos = [
            mouse_pos[0] - mouse_pos[0] % offset,
            mouse_pos[1] - mouse_pos[1] % offset
        ]
        grid_poses = list(map(lambda elem: elem.saved_pos, sprites_array))
        
        for x in range(-grid_size, grid_size):
            for y in range(-grid_size, grid_size):
                pos = [
                    mouse_pos[0] + x * offset,
                    mouse_pos[1] + y * offset
                ]
                
                if pos not in grid_poses:
                    sprite = MySprite(pos).link_texture(random.choice(grass_textures), True)
                    sprite.set_typed_origin(OriginTypes.DOWN_CENTER)
                    sprite.set_scale(10)
                    sprite.set_position(Vec2f.from_array(pos)+Vec2f.random()*offset*2)
                    
                    sprites_array.append(sprite)

        sprites_array = list(sorted(sprites_array, key=lambda elem: elem.saved_pos[1]))

radius = 100

def update_sprite_array(worker: CycleWorker):
    global sprites_array
    press = False
    if MouseInterface.get_press('right'):
        press = True
    
    mp = MouseInterface.get_position_in_window(window)
    for sprite in sprites_array:
        this_angle = math.sin(sprite.saved_pos[0] / 300 + sprite.saved_pos[1] / 300 + window.get_global_timer(2)) * 20
        
        
        if press and (sprite.get_position_x() - mp.x)**2 + (sprite.get_position_y() - mp.y)**2 < radius**2:
            if sprite.get_position_x() - mp.x >= 0:
                this_angle += 100-math.sqrt((sprite.get_position_x() - mp.x)**2 + (sprite.get_position_y() - mp.y)**2) / radius * 90
            else:
                this_angle -= 100-math.sqrt((sprite.get_position_x() - mp.x)**2 + (sprite.get_position_y() - mp.y)**2) / radius * 90
        sprite.saved_angle = this_angle
        sprite.angle += (sprite.saved_angle - sprite.angle) / 10
        sprite.set_rotation(sprite.angle)
        

        if MouseInterface.get_press("middle") and (sprite.get_position_x() - mp.x)**2 + (sprite.get_position_y() - mp.y)**2 < radius**2:
            sprites_array.remove(sprite)

worker = CycleWorker()
worker.set_delay(1/180)
worker.set_daemon(True)
worker.start(update_sprite_array)

def draw_sprites_array():
    global sprites_array
    
    for sprite in sprites_array:
        window.draw(sprite)

while window.update(events):
    window.clear(Color.from_hex("847e87"))
    
    if events.get_type() == events.Type.MouseWheelMoved:
        radius += events.get_mouse_wheel() * 10
    
    
    draw_sprites_array()
    draw_grass(5, 30)

    window.view_info()
    window.display()
